import random


class Banners:
    DEFAULT_BANNER = "*********************************************************\n" \
                     "*      _    _                          _                *\n" \
                     "*     |  \/  |                        (_)               *\n" \
                     "*     | .  . | ___ _ __ ___ _   _ _ __ _ _   _ ___      *\n" \
                     "*     | |\/| |/ _ \ '__/ __| | | | '__| | | | / __|     *\n" \
                     "*     | |  | |  __/ | | (__| |_| | |  | | |_| \__ \     *\n" \
                     "*     \_|  |_/\___|_|  \___|\__,_|_|  |_|\__,_|___/     *\n" \
                     "*                                                       *\n" \
                     "* Mercurius  v1.0.0                                     *\n" \
                     "* Ilario Dal Grande                                     *\n" \
                     "* http://silentfrog.net                                 *\n" \
                     "* ilario.dalgrande@silentfrog.net                       *\n" \
                     "*********************************************************\n"

    @classmethod
    def get_random_banner(cls):
        banners = [cls.DEFAULT_BANNER]

        return random.choice(banners)
