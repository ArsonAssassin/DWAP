import os
from typing import Optional

import Utils
import settings
from worlds.Files import APProcedurePatch, APTokenMixin


DW1_HASH = "8520edac0f7f1454f8a008ac5e599c1a"


class DW1ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = DW1_HASH
    game = "Digimon World"
    patch_file_ending = ".apdw1"
    result_file_ending = ".bin"

    procedure = [
        ("apply_bsdiff4", ["dw1_iso.bsdiff4"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


class DW1Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Digimon World (USA) BIN image"""
        description = "Digimon World (USA) BIN file"
        copy_to = "Digimon World (USA).bin"
        md5s = [DW1_HASH]

    rom_file: RomFile = RomFile("Digimon World (USA).bin")


def get_base_rom_bytes(file_name: Optional[str] = None) -> bytes:
    file_name = file_name or get_base_rom_path()
    with open(file_name, "rb") as f:
        return f.read()


def get_base_rom_path(file_name: Optional[str] = None) -> str:
    if file_name is None:
        file_name = "Digimon World (USA).bin"
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
