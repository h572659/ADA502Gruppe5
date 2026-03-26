class indicator:
    # NOTE: WIP - We may wish to provide different and more nuanced feedback
    def indication(self, ttf):
            if ttf < 5:
                return "red"
            elif ttf > 10:
                return "green"
            else:
                return "yellow"


def indication(ttf):
    return indicator().indication(ttf)
        