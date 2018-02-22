from widget import Widget

recipes = ["AEDCA", "BEACD", "BABCE", "DADBD", "BECBD"]
widgets = [Widget(i) for i in recipes]

print(widgets)

distances = { "A": {"B": 1064,
                    "C": 673,
                    "D": 1401,
                    "E": 277},
              "B": {"A": 1064,
                    "C": 958,
                    "D": 1934,
                    "E": 337},
              "C": {"A": 673,
                    "B": 958,
                    "D": 1001,
                    "E": 399},
              "D": {"A": 1401,
                    "B": 1934,
                    "C": 1001,
                    "E": 387},
              "E": {"A": 277,
                    "B": 337,
                    "C": 399,
                    "D": 387}}
