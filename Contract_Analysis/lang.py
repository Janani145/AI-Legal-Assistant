import argostranslate.package
import argostranslate.translate

argostranslate.package.update_package_index()
packages = argostranslate.package.get_available_packages()

for p in packages:
    if p.from_code == "hi" and p.to_code == "en":
        argostranslate.package.install_from_path(p.download())
