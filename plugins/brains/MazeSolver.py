try:
    from pyrobot.brain import Brain
except ImportError:
    class Robot:
        th = 10
    class Brain:
        pass

class MazeSolver(Brain):
    def setup(self):
        self.debug = True
        self.dist = 0.25
        self.side_wall_dist = 0.7
        self.speed = 0.3
        self.degree = 0.3 # 10 degrees?
        self.target_degree = 0.0
        self.rotating = False
        self.parallel = False
        self.step_count = 0
        self.wall_missing = False
        self.left_side_open = False
        self.parallel_check_steps = 50
        self.parallel_checks = 0
        self.max_parallel_checks = 50
        self.translation = 0
        self.side_wall_correction_done = False
        self.current_message = ""
        self.message_shown_steps = 0
        self.max_message_show_steps = 20

    def set_message(self, message, max_steps = 20):
        self.current_message = message
        self.message_shown_steps = 0
        self.max_message_show_steps = max_steps

    def show_message(self):
        if self.message_shown_steps > self.max_message_show_steps:
            self.set_message("")
        if self.message_shown_steps == 0:
            self.robot.speech[0].say(self.current_message)
        self.message_shown_steps += 1

    def get_min_distance(self, range_name):
        range = self.robot.range[range_name]
        return min([s.distance() for s in range])

    def is_left_side_open(self):
        # robot has passed the wall on left, now it has to turn left and move
        if self.leftFront > self.side_wall_dist and self.leftBack > self.side_wall_dist and self.leftBackCorner > self.side_wall_dist:
            self.left_side_open = True
        return self.left_side_open

    def is_right_side_open(self):
        return self.rightFront > self.side_wall_dist and self.rightBack > self.side_wall_dist

    def find_target_degree(self, degree):
        target_degree = self.robot.th + degree
        if target_degree > 359:
            target_degree = target_degree - 359
        elif target_degree < 0:
            target_degree = 359 + target_degree

        return target_degree

    def show_debug(self, *args):
        if self.debug:
            print args

    def determineMove(self):
        translation = 0.0
        rotate = 0.0

        # check if there is a wall in front
        if self.front < self.dist:
            self.left_side_open = False
            # check if there is no wall in left
            if self.is_left_side_open():
                rotate = self.degree
                self.target_degree = self.find_target_degree(90.0)
                self.set_message("Front blocked, Left open, rotate 90")
                self.show_debug("left side open", self.target_degree)
            # check if there is no wall in right
            elif self.is_right_side_open():
                rotate = self.degree * -1.0
                self.target_degree = self.find_target_degree(-90.0)
                self.set_message("Front blocked, Right open, rotate 90")
                self.show_debug("right side open", self.target_degree)
            # walls on left and right, turn around
            else:
                rotate = self.degree
                self.target_degree = self.find_target_degree(180.0)
                self.set_message("All blocked, turn around")
                self.show_debug("turn around", self.target_degree)
        elif self.left_side_open:
            if abs(self.robot_x - self.robot.x) > 0.8 or abs(self.robot_y - self.robot.y) > 0.8:
                self.left_side_open = False
            else:
                translation = self.speed
        # check if left side is open
        elif self.is_left_side_open():
            rotate = self.degree
            self.target_degree = self.find_target_degree(90.0)
            self.set_message("Left open, rotate 90")
            self.show_debug("front free, left free", self.target_degree)
        # if wall on left and no wall in front, move forward
        else:
            translation = self.speed

        return translation, rotate

    def assign_distances(self):
        self.front = self.get_min_distance('front')
        self.leftFront = self.get_min_distance('left-front')
        self.leftBack = self.get_min_distance('left-back')
        self.leftBackCorner = self.robot.range[14].distance()
        self.rightFront = self.get_min_distance('right-front')
        self.rightBack = self.get_min_distance('right-back')
        self.rightBackCorner = self.robot.range[9].distance()

    def is_target_degree_achieved(self):
        degree_diff = max(self.robot.th, self.target_degree) - min(self.robot.th, self.target_degree)
        return degree_diff <= 3.0

    def is_parallel(self):
        if not self.parallel:
            diffLeft = max(self.leftFront, self.leftBack) - min(self.leftFront, self.leftBack)
            diffRight = max(self.rightFront, self.rightBack) - min(self.rightFront, self.rightBack)
            if abs(diffLeft - diffRight) > 0.1:
                diff = min(diffLeft, diffRight)
            else:
                diff = diffLeft

            self.parallel = diff < 0.005
        return self.parallel

    def get_rotate_for_parallel(self):
        if self.leftFront < self.rightFront:
            if self.leftFront < self.leftBack:
                return -1.0 * 0.1 # turn right
            elif self.leftFront > self.leftBack:
                return 0.1 # turn left
        else:
            if self.rightFront > self.rightBack:
                return -1.0 * 0.1 # turn right
            elif self.rightFront < self.rightBack:
                return 0.1 # turn left

        return 0.0 # no turn

    def is_too_close_to_side_wall(self):
        if self.side_wall_correction_done:
            return False
        if self.leftFront < self.dist:
            return True
        elif self.rightFront < self.dist:
            return True
        return False

    def step(self):
        self.assign_distances()

        if self.rotating:
            if self.is_target_degree_achieved():
                self.set_message("Rotation finished", 5)
                self.rotating = False
                self.parallel = False
                self.target_degree = 0
                self.step_count = 0
                self.parallel_checks = 0
                self.robot_x = self.robot.x
                self.robot_y = self.robot.y
                self.side_wall_correction_done = False
        else:
            if not self.is_parallel():
                self.parallel_checks += 1
                if self.parallel_checks > self.max_parallel_checks:
                    self.parallel_checks = 0
                    self.robot.move(0.1, 0.0)
                else:
                    rotate = self.get_rotate_for_parallel()
                    self.robot.move(0.0, rotate)
            elif not self.side_wall_correction_done and self.is_too_close_to_side_wall():
                if self.leftFront < self.dist:
                    rotate = -1.0 * 0.1
                else:
                    rotate = 1.0 * 0.1
                self.robot.move(0, rotate)
                self.side_wall_correction_done = True
                self.set_message("Too close to wall", 5)
            else:
                self.translation, self.rotate = self.determineMove()
                self.rotating = self.rotate != 0
                self.robot.move(self.translation, self.rotate)
                self.step_count += 1
                # toggle check for parallel after each n steps
                if self.step_count > self.parallel_check_steps:
                    self.set_message("Check if parallel", 5)
                    self.step_count = 0
                    self.parallel = False
                    self.side_wall_correction_done = False

        self.show_message()



def INIT(engine):
    assert (engine.robot.requires("range-sensor") and
            engine.robot.requires("continuous-movement"))
    return MazeSolver('MazeSolver', engine)

