class indicator:

    def indication(self, ttf):
            if ttf < 5:
                return "red"
            elif ttf > 10:
                return "green"
            else:
                return "yellow"
        