import sh
from pythonforandroid.logger import shprint
from pythonforandroid.recipe import IncludedFilesBehaviour, CythonRecipe
from pythonforandroid.util import current_directory


class MidistreamRecipe(IncludedFilesBehaviour, CythonRecipe):
    name = "midistream"
    depends = ["audiostream"]
    src_filename = "../../midistream"

    def get_recipe_env(self, arch=None):
        env = super().get_recipe_env(arch)
        build_dir = self.get_build_dir(arch.arch)
        env["LDFLAGS"] += " -L" + build_dir
        env["LDFLAGS"] += " -lsonivox"
        return env

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        cli = env["CC"].split()
        cmd = sh.Command(cli[0])
        flags = cli[1:]

        with current_directory(self.get_build_dir(arch.arch)):
            # create fake (empty) shared library libsonivox.so
            shprint(cmd, *flags, "-shared", "-o", "libsonivox.so", "-fPIC", "-xc", "/dev/null")
            pass

        super().build_arch(arch)


recipe = MidistreamRecipe()
