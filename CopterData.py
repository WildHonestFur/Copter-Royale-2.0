class Data:
    # --- Global ---
    powernames = ["Speed", "Sniper", "Invisibility", "Rapid Fire", "Homing Shots", "Dash", "Regeneration", "Blast", "Teleport", "Shield",
                  "Shotgun", "Backshots", "Dual Fire", "Surge Shot", "Randomizer"]
    powermap = {
        "Speed": "speed",
        "Sniper": "sniper",
        "Invisibility": "invis",
        "Rapid Fire": "rapid fire",
        "Homing Shots": "homing",
        "Surge Shot": "charge",
        "Dash": "dash",
        "Regeneration": "regen",
        "Blast": "blast",
        "Teleport": "teleport",
        "Shield": "shield",
        "Shotgun": "shotgun",
        "Backshots": "backshot",
        "Dual Fire": "double",
        "Randomizer": "random"
    }

    powerdata = {
        "speed": [12, 25],
        "sniper": [10, 35],
        "invis": [8, 30],
        "rapid fire": [12, 25],
        "homing": [10, 30],
        "charge": [10, 25],
        "dash": [0.2, 8],
        "regen": [5, 25],
        "blast": [0.5, 20],
        "teleport": [1, 12],
        "shield": [10, 25],
        "shotgun": [10, 30],
        "backshot": [12, 25],
        "double": [15, 25],
        "random": [8, 17]
    }
    
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
        self.chosen = 'Speed'
        self.lasttime = 0
        self.choosing = 0
        self.power = ''
        self.health = 100
        self.x = 0
        self.y = 0
        self.angle = 0
        self.bullets = []
        self.lastbullet = -1

        self.enemies = []
        self.ebullets = []
        
