from _hidden_kit import check, find, load, report

badges = load("events.badges")
badge = find(badges, "badge_text")

correct = (badge is not None
           and check("plain names", lambda: badge("ada", "lovelace", "AE") == "Ada Lovelace - AE"
                     and badge("GRACE", "hopper", "Navy") == "Grace Hopper - Navy"))
quality = (check("particles stay lower case, like the rest of the app",
                 lambda: badge("ludwig", "van beethoven", "Bonn Opera") == "Ludwig van Beethoven - Bonn Opera"
                 and badge("marie", "DE LA TOUR", "Paris Lab") == "Marie de la Tour - Paris Lab")
           and check("hyphens and apostrophes", lambda: badge("anne-marie", "o'neil", "Dublin") == "Anne-Marie O'Neil - Dublin"))
report(correct, quality=quality)
