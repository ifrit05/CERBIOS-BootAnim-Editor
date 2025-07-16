import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import tkinter.filedialog as fd
import tkinter.colorchooser as cc
import re

# Required keys
DEFAULTS = {
    "CameraMode": "0",

    "PlasmaRender": "true",
    "Plasma1": "#0000FF",
    "Plasma2": "#0000FF",
    "Plasma3": "#0000FF",

    "ShieldRender": "true",
    "ShieldWireframe": "true",
    "Shield": "#FF00FF",

    "BlobRender": "true",
    "BlobWireframe": "true",
    "BlobColor": "#283FFF",
    "BlobGlow": "#A040FF",

    "SceneRender": "true",
    "SceneWireframe": "false",
    "SceneIntensity": "2",
    "SceneAmbient": "#3519FF",
    "SceneDiffuse": "#3519FF",
    "SceneSpecular": "#3519FF",

    "SlashBackgroundStart": "#000000",
    "SlashBackgroundEnd": "#FFFFFF",
    "SlashLipGradientStart": "#000100",
    "SlashLipGradientEnd": "#7A7AFF",
    "SlashInnerStage1Gradient1": "#FFFFFF",
    "SlashInnerStage1Gradient2": "#FFFFFF",
    "SlashInnerStage1Gradient3": "#7A7AFF",
    "SlashInnerStage1Gradient4": "#7A7AFF",
    "SlashInnerStage2Gradient1": "#7A7AFF",
    "SlashInnerStage2Gradient2": "#7A7AFF",
    "SlashInnerStage2Gradient3": "#CCCCFF",
    "SlashInnerStage2Gradient4": "#0000D6",

    "TradeMarkRender": "true",
    "TradeMark": "#7477FF",

    "XboxRender": "true",
    "Xbox": "#7477FF",

    "BrandRender": "true",
    "Brand": "#7477FF"
}

TAB_NAMES = [
    "Camera Mode",    # 1
    "Plasma",         # 2
    "Shield",         # 3
    "Blob",           # 4
    "Background",     # 5
    "X Splash",       # 6
    "TradeMark Logo",      # 7
    "Xbox Text",      # 8
    "CERBIOS Text"    # 9
]

def load_ini(filepath):
    grouped_data = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    group = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith(';'):
            if group:
                grouped_data.append(group)
                group = []
        elif '=' in line:
            group.append(tuple(map(str.strip, line.split('=', 1))))
    if group:
        grouped_data.append(group)

    while len(grouped_data) < len(TAB_NAMES):
        grouped_data.append([])

    return grouped_data[:len(TAB_NAMES)]

def is_boolean(value):
    return value.lower() in ['true', 'false']

def is_color(value):
    return re.match(r'^#([A-Fa-f0-9]{6})$', value.strip()) is not None

def create_color_input(parent, var):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=6)

    entry = ctk.CTkEntry(row, textvariable=var, width=100)
    entry.pack(side="left", padx=(0, 5))

    preview = ctk.CTkLabel(row, text="", width=20, height=20, corner_radius=4)
    preview.pack(side="left", padx=5)

    def update_preview(*_):
        value = var.get()
        if is_color(value):
            preview.configure(fg_color=value)
            entry.configure(border_color="gray", border_width=1)
        else:
            preview.configure(fg_color="transparent")
            entry.configure(border_color="red", border_width=2)

    var.trace_add("write", update_preview)
    update_preview()

    def choose_color():
        color = cc.askcolor(color=var.get())[1]
        if color:
            var.set(color)

    pick_button = ctk.CTkButton(row, text="Pick", command=choose_color, width=60)
    pick_button.pack(side="left")
    return row

def build_ui(root, ini_path, parsed_groups):
    entries = {}

    tabview = ctk.CTkTabview(root)
    tabview.pack(fill="both", expand=True, padx=10, pady=10)

    for tab_index, tab_name in enumerate(TAB_NAMES):
        tab = tabview.add(tab_name)
        tab_frame = ctk.CTkFrame(tab, fg_color="transparent")
        tab_frame.pack(fill="both", expand=True, padx=10, pady=10)

        group = parsed_groups[tab_index] if tab_index < len(parsed_groups) else []

        # Special layout for X Splash
        if tab_name == "X Splash":
            columns_frame = ctk.CTkFrame(tab_frame, fg_color="transparent")
            columns_frame.pack(fill="both", expand=True)

            left_col = ctk.CTkFrame(columns_frame, fg_color="transparent")
            left_col.pack(side="left", fill="both", expand=True, padx=10)

            right_col = ctk.CTkFrame(columns_frame, fg_color="transparent")
            right_col.pack(side="left", fill="both", expand=True, padx=10)

            for idx, (key, value) in enumerate(group):
                target_col = left_col if idx % 2 == 0 else right_col
                row = ctk.CTkFrame(target_col, fg_color="transparent")
                row.pack(fill="x", pady=4)

                ctk.CTkLabel(row, text=key, width=180, anchor="w").pack(side="left")

                if is_boolean(value):
                    var = ctk.BooleanVar(value=value.lower() == 'true')
                    switch = ctk.CTkSwitch(row, variable=var, text="")
                    switch.pack(side="left")
                    entries[(tab_name, key)] = lambda v=var: 'true' if v.get() else 'false'

                elif is_color(value):
                    var = ctk.StringVar(value=value)
                    create_color_input(row, var)
                    entries[(tab_name, key)] = var

                else:
                    var = ctk.StringVar(value=value)
                    entry = ctk.CTkEntry(row, textvariable=var)
                    entry.pack(side="left", fill="x", expand=True)
                    entries[(tab_name, key)] = var

        else:
            for key, value in group:
                row = ctk.CTkFrame(tab_frame, fg_color="transparent")
                row.pack(fill="x", pady=4)

                ctk.CTkLabel(row, text=key, width=180, anchor="w").pack(side="left")

                if is_boolean(value):
                    var = ctk.BooleanVar(value=value.lower() == 'true')
                    switch = ctk.CTkSwitch(row, variable=var, text="")
                    switch.pack(side="left")
                    entries[(tab_name, key)] = lambda v=var: 'true' if v.get() else 'false'

                elif is_color(value):
                    var = ctk.StringVar(value=value)
                    create_color_input(row, var)
                    entries[(tab_name, key)] = var

                else:
                    var = ctk.StringVar(value=value)

                    if tab_name == "Camera Mode" and key == "CameraMode":
                        combo = ctk.CTkComboBox(
                            row,
                            variable=var,
                            values=[str(i) for i in range(15)],
                            width=100
                        )
                        combo.pack(side="left")
                    else:
                        entry = ctk.CTkEntry(row, textvariable=var)
                        entry.pack(side="left", fill="x", expand=True)

                entries[(tab_name, key)] = var


    save_btn = ctk.CTkButton(root, text="Save", command=lambda: save_changes(ini_path, parsed_groups, entries))
    save_btn.pack(pady=20)

def save_changes(filepath, parsed_groups, entries):
    with open(filepath, 'w') as f:
        for tab_index, tab_name in enumerate(TAB_NAMES):
            group = parsed_groups[tab_index] if tab_index < len(parsed_groups) else []
            f.write(f"; {tab_name}\n")
            for key, _ in group:
                val = entries.get((tab_name, key))
                result = val() if callable(val) else val.get()
                f.write(f"{key} = {result}\n")
            f.write("\n")

def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.title("Cerbios BootAnim Editor")
    root.geometry("850x450")
    root.resizable(False, False)

    ini_path = fd.askopenfilename(
        title="Select bootanim.ini file",
        filetypes=[("INI Files", "*.ini")]
    )

    # Check filename
    if not ini_path or not ini_path.lower().endswith("bootanim.ini"):
        CTkMessagebox(
            title="Invalid File",
            message="You must select a file named exactly 'bootanim.ini'.",
            icon="cancel"
        )
        root.destroy()
        return

    parsed_groups = load_ini(ini_path)
    current_entries = {key: val for group in parsed_groups for key, val in group}

    # Compare keys
    current_keys = set(current_entries.keys())
    valid_keys = set(DEFAULTS.keys())

    unknown_keys = current_keys - valid_keys
    missing_keys = valid_keys - current_keys

    if unknown_keys or missing_keys:
        msg_lines = []
        if missing_keys:
            msg_lines.append("Missing Keys:\n" + "\n".join(f"• {k}" for k in sorted(missing_keys)))
        if unknown_keys:
            msg_lines.append("Unknown Keys:\n" + "\n".join(f"• {k}" for k in sorted(unknown_keys)))

        result = CTkMessagebox(
            title="bootanim.ini Invalid",
            message="\n\n".join(msg_lines) + "\n\nWould you like to repair it automatically?",
            icon="warning",
            option_1="Repair and Continue",
            option_2="Cancel"
        ).get()

        if result == "Repair and Continue":
            # Apply repair
            repaired = {k: current_entries.get(k, DEFAULTS[k]) for k in DEFAULTS.keys()}

            # Rewrite file
            with open(ini_path, 'w') as f:
                for tab_name in TAB_NAMES:
                    f.write(f"; {tab_name}\n")
                    for key in repaired:
                        if key in DEFAULTS and get_tab_for_key(key) == tab_name:
                            f.write(f"{key} = {repaired[key]}\n")
                    f.write("\n")

            # Reload valid file
            parsed_groups = load_ini(ini_path)

        else:
            root.destroy()
            return

    # Valid or repaired — load UI
    build_ui(root, ini_path, parsed_groups)
    root.mainloop()

def get_tab_for_key(key):
    # Maps each key to its tab index based on expected groupings (same as TAB_NAMES)
    tab_map = {
        "CameraMode": "Camera Mode",

        "PlasmaRender": "Plasma", "Plasma1": "Plasma", "Plasma2": "Plasma", "Plasma3": "Plasma",

        "ShieldRender": "Shield", "ShieldWireframe": "Shield", "Shield": "Shield",

        "BlobRender": "Blob", "BlobWireframe": "Blob", "BlobColor": "Blob", "BlobGlow": "Blob",

        "SceneRender": "Background", "SceneWireframe": "Background", "SceneIntensity": "Background",
        "SceneAmbient": "Background", "SceneDiffuse": "Background", "SceneSpecular": "Background",

        "SlashBackgroundStart": "X Splash", "SlashBackgroundEnd": "X Splash",
        "SlashLipGradientStart": "X Splash", "SlashLipGradientEnd": "X Splash",
        "SlashInnerStage1Gradient1": "X Splash", "SlashInnerStage1Gradient2": "X Splash",
        "SlashInnerStage1Gradient3": "X Splash", "SlashInnerStage1Gradient4": "X Splash",
        "SlashInnerStage2Gradient1": "X Splash", "SlashInnerStage2Gradient2": "X Splash",
        "SlashInnerStage2Gradient3": "X Splash", "SlashInnerStage2Gradient4": "X Splash",

        "TradeMarkRender": "TradeMark Logo", "TradeMark": "TradeMark Logo",
        "XboxRender": "Xbox Text", "Xbox": "Xbox Text",
        "BrandRender": "CERBIOS Text", "Brand": "CERBIOS Text"
    }
    return tab_map.get(key, "Other")

if __name__ == "__main__":
    main()