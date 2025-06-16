class Data:
    def __init__(self):
        # --- Game control ---
        self.frame = "login"
        self.running = True

        # --- Login part ---
        self.active_box = None
        self.username_text = ""
        self.password_text = ""
        self.loginerror = ""
        self.user = None

        # --- Home part ---
        self.pcolor = (0, 0, 0)
        self.changecolor = False
        self.name = ""

        # --- Stats part ---
        self.user_stats = {
            "Games Won": None,
            "Top 3 Finishes": None,
            "Total Kills": None,
            "Average Kills": None,
            "Max Kills": None
        }

        # --- Leaderboard part ---
        self.selected_tab = "Games Won"
        self.leaderboard_data = {}

        # --- Waiting part ---
        self.barsize = 0
        self.bargoal = 0
        self.lastcheck = -1

        # --- End part ---
        self.killcount = 0
        self.message = ''
        self.place = 0

        # --- Game part ---
        self.host = False
        self.mode = 'off'
        self.power = ''
        self.health = 100
        self.x = 0
        self.y = 0
        self.angle = 0
        self.bullets = []
        self.lastbullet = -1
