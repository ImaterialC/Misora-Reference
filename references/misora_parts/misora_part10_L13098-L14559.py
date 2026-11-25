# misora.py PART 10/12 | ORIG L13098-L14559/17315 | SHA:ec4d9bfc8ec6
# SYMS: L13098:MisoraApp.on_open_paths_dialog, L13305:MisoraApp._toggle_side_drawer_pin, L13315:MisoraApp.on_open_mtl_settings, L13319:MisoraApp.on_open_ai_prompt_settings, L13323:MisoraApp.on_open_translator_assistant, L13340:MisoraApp._build_mtl_tab, L13466:MisoraApp._build_mtl_all_script_pane, L13615:MisoraApp._apply_mtl_all_script_theme_tags, L13638:MisoraApp._set_mtl_drawer_mode, L13682:MisoraApp._set_mtl_drawer_engine_enabled, L13690:MisoraApp._on_mtl_drawer_engine_toggled, L13696:MisoraApp._rebuild_mtl_drawer_cards, L13823:MisoraApp._get_mtl_drawer_active_box, L13832:MisoraApp._refresh_mtl_drawer_box, L13890:MisoraApp._mtl_drawer_cache_put, L13897:MisoraApp._on_mtl_drawer_refresh_all, L13937:MisoraApp._on_mtl_drawer_refresh_engine, L13941:MisoraApp._dispatch_mtl_drawer_engine, L13998:MisoraApp._poll_mtl_drawer_queue, L14084:MisoraApp._on_mtl_drawer_apply_engine, L14140:MisoraApp._is_mtl_empty_or_punct, L14150:MisoraApp._mtl_all_ctx_key, L14154:MisoraApp._find_box_index_by_uid, L14163:MisoraApp._flush_mtl_all_scratchpad, L14180:MisoraApp._load_mtl_all_scratchpad, L14223:MisoraApp._on_mtl_all_engine_changed, L14227:MisoraApp._on_mtl_all_list_click, L14249:MisoraApp._refresh_mtl_all_script_view, L14334:MisoraApp._dispatch_mtl_all_box, L14384:MisoraApp._on_mtl_all_script_refresh_selected, L14402:MisoraApp._on_mtl_all_script_apply_selected, L14453:MisoraApp._on_mtl_all_script_translate_all, L14482:MisoraApp._on_mtl_all_script_apply_all

    def on_open_paths_dialog(self) -> None:
        """Dialog to configure Backup Folder, Project/Mod Folder, Datamine Tool, External Editors, Config, and Debug Log."""
        t = self.theme
        dlg = tk.Toplevel(self)
        dlg.title("Configure Paths, Backups & Folders")
        dlg.geometry("660x540")
        dlg.minsize(600, 480)
        dlg.transient(self)
        dlg.grab_set()
        dlg.configure(bg=t["bg_panel"])

        fg_panel = best_contrast_fg(t["bg_panel"])
        fg_editor = best_contrast_fg(t["bg_editor"])

        # 1. Pack bottom button bar FIRST so it stays anchored and visible
        btn_bar = tk.Frame(dlg, bg=t["bg_panel"], padx=16, pady=12)
        btn_bar.pack(side="bottom", fill="x")

        # 2. Main content frame
        content = tk.Frame(dlg, bg=t["bg_panel"], padx=16, pady=12)
        content.pack(side="top", fill="both", expand=True)

        def make_row(parent, label_text: str, browse_cmd=None, open_cmd=None, browse_text="Browse..."):
            r = tk.Frame(parent, bg=t["bg_panel"])
            r.pack(fill="x", pady=4)
            lbl = tk.Label(r, text=label_text, font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"], width=24, anchor="w")
            lbl.pack(side="left")
            if browse_cmd:
                btn_b = ttk.Button(r, text=browse_text, style="Small.TButton", command=browse_cmd)
                btn_b.pack(side="right", padx=(4, 0))
            if open_cmd:
                btn_o = ttk.Button(r, text="Open", style="Small.TButton", command=open_cmd)
                btn_o.pack(side="right", padx=(4, 0))
            ent = tk.Entry(r, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid")
            ent.pack(side="left", fill="x", expand=True, padx=4)
            return r, ent

        # 1. Backup Folder
        def _browse_bak():
            d = filedialog.askdirectory(title="Select Backup Folder")
            if d:
                ent_backup.delete(0, tk.END)
                ent_backup.insert(0, d)
                var_use_default_bak.set(False)

        def _open_bak_folder():
            b = ent_backup.get().strip() or str(SCRIPT_DIR / "backups")
            p = Path(b)
            p.mkdir(parents=True, exist_ok=True)
            subprocess.Popen(["explorer.exe", str(p)])

        r1, ent_backup = make_row(content, "Backup Folder:", browse_cmd=_browse_bak, open_cmd=_open_bak_folder)
        cur_bak = str(self.backup_folder) if self.backup_folder else str(SCRIPT_DIR / "backups")
        ent_backup.insert(0, cur_bak)
        var_use_default_bak = tk.BooleanVar(master=dlg, value=(self.backup_folder is None))

        cb_bak = tk.Checkbutton(
            content,
            text="Use default backups folder (SCRIPT_DIR/backups)",
            variable=var_use_default_bak,
            bg=t["bg_panel"],
            fg=fg_panel,
            selectcolor=t["bg_dark"],
            activebackground=t["bg_panel"],
            activeforeground=fg_panel,
        )
        cb_bak.pack(anchor="w", padx=(170, 0), pady=(0, 6))

        # 2. Project / Mod Root Folder (BepInEx, MelonLoader, XUAT, custom)
        def _browse_project():
            init_d = ent_project.get().strip() or self._get_project_display_path()
            d = filedialog.askdirectory(initialdir=init_d, title="Select Project Root / Mod Folder (BepInEx, MelonLoader, etc.)")
            if d:
                ent_project.delete(0, tk.END)
                ent_project.insert(0, d)

        def _open_project_folder_ui():
            b = ent_project.get().strip() or self._get_project_display_path()
            if b and Path(b).exists():
                subprocess.Popen(["explorer.exe", str(b)])
            else:
                messagebox.showinfo("Project Folder", "Folder does not exist.")

        r2, ent_project = make_row(content, "Project / Mod Folder:", browse_cmd=_browse_project, open_cmd=_open_project_folder_ui)
        cur_proj = str(self.project_folder) if getattr(self, "project_folder", None) else self._get_project_display_path()
        ent_project.insert(0, cur_proj)

        lbl_proj_hint = tk.Label(
            content,
            text="Root directory for translation/mod project (BepInEx, MelonLoader, XUAT, etc.)",
            font=("Segoe UI", 8),
            bg=t["bg_panel"],
            fg=t["fg_muted"]
        )
        lbl_proj_hint.pack(anchor="w", padx=(170, 0), pady=(0, 6))

        # 3. Universal Datamine Tool
        def _browse_datamine():
            f = filedialog.askopenfilename(
                title="Select Datamine Tool",
                filetypes=[("Executables & Scripts", "*.exe;*.py;*.bat;*.cmd"), ("All Files", "*.*")]
            )
            if f:
                ent_datamine.delete(0, tk.END)
                ent_datamine.insert(0, f)

        r3, ent_datamine = make_row(content, "Datamine Tool:", browse_cmd=_browse_datamine)
        if self.datamine_exe:
            ent_datamine.insert(0, str(self.datamine_exe))

        # 4. Notepad++ Path
        def _browse_npp():
            f = filedialog.askopenfilename(
                title="Select Notepad++ Executable",
                filetypes=[("Executables", "*.exe"), ("All Files", "*.*")]
            )
            if f:
                ent_npp.delete(0, tk.END)
                ent_npp.insert(0, f)

        r4, ent_npp = make_row(content, "Notepad++ Executable:", browse_cmd=_browse_npp)
        if self.notepadpp_path:
            ent_npp.insert(0, str(self.notepadpp_path))

        # 5. External Text Editor
        def _browse_editor():
            f = filedialog.askopenfilename(
                title="Select External Text Editor",
                filetypes=[("Executables & Scripts", "*.exe;*.bat;*.cmd"), ("All Files", "*.*")]
            )
            if f:
                ent_editor.delete(0, tk.END)
                ent_editor.insert(0, f)

        r5, ent_editor = make_row(content, "External Text Editor:", browse_cmd=_browse_editor)
        if self.external_editor_path:
            ent_editor.insert(0, str(self.external_editor_path))

        # Separator & File references
        ttk.Separator(content, orient="horizontal").pack(fill="x", pady=10)

        # 6. Config File
        r_cfg = tk.Frame(content, bg=t["bg_panel"])
        r_cfg.pack(fill="x", pady=2)
        tk.Label(r_cfg, text="Config File:", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["fg_muted"], width=24, anchor="w").pack(side="left")
        ttk.Button(r_cfg, text="Reveal", style="Small.TButton", command=lambda: subprocess.Popen(["explorer.exe", f"/select,{CONFIG_PATH}"])).pack(side="right", padx=(4, 0))
        tk.Label(r_cfg, text=str(CONFIG_PATH), font=("Consolas", 8), bg=t["bg_panel"], fg=fg_panel, anchor="w").pack(side="left", fill="x", expand=True)

        # 7. Debug Log
        r_log = tk.Frame(content, bg=t["bg_panel"])
        r_log.pack(fill="x", pady=2)
        tk.Label(r_log, text="Debug Log:", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["fg_muted"], width=24, anchor="w").pack(side="left")
        ttk.Button(r_log, text="Open", style="Small.TButton", command=self._on_open_debug_log_file).pack(side="right", padx=(4, 0))
        tk.Label(r_log, text=str(DEBUG_LOG_PATH), font=("Consolas", 8), bg=t["bg_panel"], fg=fg_panel, anchor="w").pack(side="left", fill="x", expand=True)

        # Buttons at bottom
        def _safe_close(_e: Optional[tk.Event] = None) -> None:
            safe_grab_release(dlg)
            if dlg.winfo_exists():
                dlg.destroy()

        def _save_and_close():
            if var_use_default_bak.get():
                self.backup_folder = None
            else:
                b_val = ent_backup.get().strip()
                self.backup_folder = Path(b_val) if b_val else None

            proj_val = ent_project.get().strip()
            if proj_val:
                p = Path(proj_val)
                self._set_project_folder(p)
                if self.scope_var.get() == "project":
                    self.folder_path_var.set(str(self.project_folder))
            else:
                self.project_folder = None
                self.bepinex_project_folder = None
                self.xuat_search_roots = []

            dm_val = ent_datamine.get().strip()
            self.datamine_exe = Path(dm_val) if dm_val else None

            npp_val = ent_npp.get().strip()
            self.notepadpp_path = Path(npp_val) if npp_val else None

            ed_val = ent_editor.get().strip()
            self.external_editor_path = Path(ed_val) if ed_val else None

            self._save_user_prefs()
            self.lbl_status.config(text="Updated paths and backup configuration.")
            self.show_toast("Paths and backup settings saved successfully!")
            _safe_close()
            messagebox.showinfo(
                "Settings Saved",
                "Paths, backups, and preferences have been saved successfully.",
                parent=self,
            )

        dlg.protocol("WM_DELETE_WINDOW", _safe_close)
        dlg.bind("<Escape>", _safe_close)

        ttk.Button(btn_bar, text="Cancel", style="TButton", command=_safe_close).pack(side="right", padx=4)
        ttk.Button(btn_bar, text="Save & Apply", style="Pink.TButton", command=_save_and_close).pack(side="right", padx=4)

    # -------------------------------------------------------------------------
    # Side Drawer Pinning (#6)
    # -------------------------------------------------------------------------
    def _toggle_side_drawer_pin(self) -> None:
        self._side_drawer_pinned = not getattr(self, "_side_drawer_pinned", False)
        pin_icon = "📌" if self._side_drawer_pinned else "📍"
        if hasattr(self, "btn_drawer_pin"):
            self.btn_drawer_pin.config(text=pin_icon)
        self.show_toast(f"Side drawer {'pinned' if self._side_drawer_pinned else 'unpinned'}")

    # -------------------------------------------------------------------------
    # Translator Suite Callbacks & Handlers (#4A, #16, #17)
    # -------------------------------------------------------------------------
    def on_open_mtl_settings(self) -> None:
        """Open the Machine Translation sources & configuration dialog."""
        MTLSettingsDialog(self)

    def on_open_ai_prompt_settings(self) -> None:
        """Open the AI / LLM translation prompt header and exporter dialog."""
        AIPromptSettingsDialog(self)

    def on_open_translator_assistant(self) -> None:
        """Toggle the docked right-side MTL Drawer tab (FEAT-12)."""
        self._toggle_side_drawer("mtl")

    # -------------------------------------------------------------------------
    # Docked Right-Side MTL Drawer — Dialogue Multi-Engine Stack (FEAT-12)
    # -------------------------------------------------------------------------
    _MTL_DRAWER_ENGINE_ORDER: Tuple[str, ...] = (
        "XUAT Cache",
        "Google",
        "DeepL",
        "Local / Sugoi",
        "LLM / OpenAI",
    )
    _MTL_DRAWER_PAID_ENGINES: Tuple[str, ...] = ("DeepL", "LLM / OpenAI")
    _MTL_DRAWER_CACHE_MAX: int = 256

    def _build_mtl_tab(self, parent: tk.Frame) -> None:
        """Build the docked MTL Drawer tab (Dialogue 1-box multi-engine stack)."""
        t = self.theme

        # Top controls: Mode selector + Refresh All
        hdr = self._tag_role(tk.Frame(parent, bg=t["bg_panel"]), "panel")
        hdr.pack(fill="x", padx=6, pady=(2, 4))

        self.btn_mtl_mode_dialogue = ttk.Button(
            hdr,
            text="Dialogue",
            style="Pink.TButton",
            command=lambda: self._set_mtl_drawer_mode("dialogue"),
        )
        self.btn_mtl_mode_dialogue.pack(side="left", padx=(0, 3))
        create_tooltip(self.btn_mtl_mode_dialogue, "Dialogue (1-Box) multi-engine stack")

        self.btn_mtl_mode_all_script = ttk.Button(
            hdr,
            text="All Script",
            style="TButton",
            command=lambda: self._set_mtl_drawer_mode("all_script"),
        )
        self.btn_mtl_mode_all_script.pack(side="left", padx=(0, 4))
        create_tooltip(self.btn_mtl_mode_all_script, "All Script batch MTL (2-widget list + scratchpad)")

        self.btn_mtl_refresh_all = ttk.Button(
            hdr,
            text="↻ Refresh All",
            style="Pink.TButton",
            command=self._on_mtl_drawer_refresh_all,
        )
        self.btn_mtl_refresh_all.pack(side="right")
        create_tooltip(self.btn_mtl_refresh_all, "Refresh all enabled engines for current box")

        # Active box context bar
        ctx_bar = self._tag_role(tk.Frame(parent, bg=t["bg_panel"]), "panel")
        ctx_bar.pack(fill="x", padx=6, pady=(0, 4))
        self._mtl_dialogue_ctx_bar = ctx_bar

        self.lbl_mtl_box_info = self._tag_role(
            tk.Label(ctx_bar, text="Box 0 / 0", bg=t["bg_panel"], fg=t["misora_pink"], anchor="w"),
            "label_accent",
        )
        self.lbl_mtl_box_info.pack(fill="x")

        self.lbl_mtl_source_preview = self._tag_role(
            tk.Label(
                ctx_bar,
                text="Open a story document to translate.",
                bg=t["bg_panel"],
                fg=t["fg_muted"],
                anchor="w",
                justify="left",
                wraplength=280,
            ),
            "label_muted",
        )
        self.lbl_mtl_source_preview.pack(fill="x", pady=(2, 0))

        # Engine visibility toggles
        eng_bar = self._tag_role(
            tk.Frame(parent, bg=t["bg_panel"], bd=1, relief="solid", highlightbackground=t["border"], highlightthickness=1),
            "panel_box",
        )
        eng_bar.pack(fill="x", padx=6, pady=(0, 4))
        self._mtl_dialogue_eng_bar = eng_bar

        self._tag_role(
            tk.Label(eng_bar, text="Enabled Engines:", bg=t["bg_panel"], fg=t["fg_muted"], anchor="w"),
            "label_muted",
        ).pack(fill="x", padx=6, pady=(4, 2))

        toggles_wrap = self._tag_role(tk.Frame(eng_bar, bg=t["bg_panel"]), "panel")
        toggles_wrap.pack(fill="x", padx=4, pady=(0, 4))

        self._mtl_drawer_engine_vars.clear()
        for eng in self._MTL_DRAWER_ENGINE_ORDER:
            enabled = bool(self._mtl_drawer_enabled_engines.get(eng, eng in ("XUAT Cache", "Google")))
            self._mtl_drawer_enabled_engines[eng] = enabled
            var = tk.BooleanVar(master=self, value=enabled)
            self._mtl_drawer_engine_vars[eng] = var
            cb = self._tag_role(
                tk.Checkbutton(
                    toggles_wrap,
                    text=eng,
                    variable=var,
                    bg=t["bg_panel"],
                    fg=best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff"),
                    selectcolor=t["bg_dark"],
                    activebackground=t["bg_panel"],
                    command=lambda e=eng: self._on_mtl_drawer_engine_toggled(e),
                ),
                "check_panel",
            )
            cb.pack(side="left", padx=(0, 4))

        # Scrollable vertical stack of enabled engine cards
        wrap = self._tag_role(tk.Frame(parent, bg=t["bg_editor"], bd=1, relief="solid"), "editor_box")
        wrap.pack(fill="both", expand=True, padx=4, pady=(0, 6))
        self._mtl_dialogue_wrap = wrap

        self._mtl_drawer_canvas = self._tag_role(
            tk.Canvas(wrap, bg=t["bg_panel"], highlightthickness=0, bd=0),
            "panel",
        )
        vscroll = tk.Scrollbar(wrap, orient="vertical", command=self._mtl_drawer_canvas.yview)
        vscroll.pack(side="right", fill="y")
        self._mtl_drawer_canvas.pack(side="left", fill="both", expand=True)
        self._mtl_drawer_canvas.configure(yscrollcommand=vscroll.set)

        self.mtl_cards_body = self._tag_role(tk.Frame(self._mtl_drawer_canvas, bg=t["bg_panel"]), "panel")
        win_id = self._mtl_drawer_canvas.create_window((0, 0), window=self.mtl_cards_body, anchor="nw")

        self.mtl_cards_body.bind(
            "<Configure>",
            lambda _e: self._mtl_drawer_canvas.configure(scrollregion=self._mtl_drawer_canvas.bbox("all")),
        )
        self._mtl_drawer_canvas.bind(
            "<Configure>",
            lambda e: self._mtl_drawer_canvas.itemconfigure(win_id, width=max(220, e.width)),
        )

        self._build_mtl_all_script_pane(parent)
        self._rebuild_mtl_drawer_cards()

    def _build_mtl_all_script_pane(self, parent: tk.Frame) -> None:
        """Build the All Script MTL mode pane: 1 single-engine selector + exact 2 tk.Text widgets (FEAT-13, NO-03)."""
        t = self.theme
        editor_fg = best_contrast_fg(t["bg_editor"], t["fg_text"], "#ffffff")

        pane = self._tag_role(tk.Frame(parent, bg=t["bg_panel"]), "panel")
        self.mtl_all_script_frame = pane

        # Top single-engine selector
        top_bar = self._tag_role(tk.Frame(pane, bg=t["bg_panel"]), "panel")
        top_bar.pack(fill="x", padx=2, pady=(0, 4))

        self._tag_role(
            tk.Label(top_bar, text="Engine:", bg=t["bg_panel"], fg=t["fg_muted"], anchor="w"),
            "label_muted",
        ).pack(side="left", padx=(0, 4))

        default_eng = getattr(self.mtl_config, "active_engine", "Google") or "Google"
        if default_eng not in self._MTL_DRAWER_ENGINE_ORDER:
            default_eng = "Google"
        self.var_mtl_all_engine = tk.StringVar(master=self, value=default_eng)
        self.cmb_mtl_all_engine = ttk.Combobox(
            top_bar,
            textvariable=self.var_mtl_all_engine,
            values=list(self._MTL_DRAWER_ENGINE_ORDER),
            state="readonly",
            width=16,
        )
        self.cmb_mtl_all_engine.pack(side="left", fill="x", expand=True)
        self.cmb_mtl_all_engine.bind("<<ComboboxSelected>>", self._on_mtl_all_engine_changed)
        create_tooltip(self.cmb_mtl_all_engine, "Select single MTL engine for All Script batch mode")

        # Action bar: Refresh Selected, Apply Selected, Translate All, Apply All
        act_bar = self._tag_role(tk.Frame(pane, bg=t["bg_panel"]), "panel")
        act_bar.pack(fill="x", padx=2, pady=(0, 4))

        self.btn_mtl_all_refresh_sel = ttk.Button(
            act_bar,
            text="↻ Refresh Selected",
            style="Small.TButton",
            command=self._on_mtl_all_script_refresh_selected,
        )
        self.btn_mtl_all_refresh_sel.pack(side="left", padx=(0, 3))
        create_tooltip(self.btn_mtl_all_refresh_sel, "Refresh selected box (bypass session cache)")

        self.btn_mtl_all_apply_sel = ttk.Button(
            act_bar,
            text="→ Apply Selected",
            style="TButton",
            command=self._on_mtl_all_script_apply_selected,
        )
        self.btn_mtl_all_apply_sel.pack(side="left", padx=(0, 3))
        create_tooltip(self.btn_mtl_all_apply_sel, "Apply scratchpad to selected box (enforces lock)")

        act_bar2 = self._tag_role(tk.Frame(pane, bg=t["bg_panel"]), "panel")
        act_bar2.pack(fill="x", padx=2, pady=(0, 4))

        self.btn_mtl_all_translate = ttk.Button(
            act_bar2,
            text="Translate All",
            style="Pink.TButton",
            command=self._on_mtl_all_script_translate_all,
        )
        self.btn_mtl_all_translate.pack(side="left", padx=(0, 3))
        create_tooltip(self.btn_mtl_all_translate, "Batch-translate all unlocked boxes (uses session cache)")

        self.btn_mtl_all_apply_all = ttk.Button(
            act_bar2,
            text="Apply All",
            style="Pink.TButton",
            command=self._on_mtl_all_script_apply_all,
        )
        self.btn_mtl_all_apply_all.pack(side="left")
        create_tooltip(self.btn_mtl_all_apply_all, "Apply all ready translations to unlocked boxes in one Undo batch")

        # Widget 1: ONE read-only multi-line tk.Text list of clickable per-box tagged blocks
        list_wrap = self._tag_role(tk.Frame(pane, bg=t["bg_editor"], bd=1, relief="solid"), "editor_box")
        list_wrap.pack(fill="both", expand=True, padx=2, pady=(0, 4))

        self.txt_mtl_all_list = self._tag_role(
            tk.Text(
                list_wrap,
                wrap="word",
                state="disabled",
                font=("Segoe UI", 9),
                bg=t["bg_editor"],
                fg=editor_fg,
                bd=0,
                padx=6,
                pady=4,
                cursor="hand2",
            ),
            "entry_editor",
        )
        list_scroll = tk.Scrollbar(list_wrap, orient="vertical", command=self.txt_mtl_all_list.yview)
        list_scroll.pack(side="right", fill="y")
        self.txt_mtl_all_list.pack(side="left", fill="both", expand=True)
        self.txt_mtl_all_list.configure(yscrollcommand=list_scroll.set)
        self.txt_mtl_all_list.bind("<Button-1>", self._on_mtl_all_list_click)

        # Widget 2: ONE shared bottom editable tk.Text scratchpad synced to clicked box
        self.lbl_mtl_all_scratch_hdr = self._tag_role(
            tk.Label(pane, text="Scratchpad (No box selected)", bg=t["bg_panel"], fg=t["misora_pink"], anchor="w"),
            "label_accent",
        )
        self.lbl_mtl_all_scratch_hdr.pack(fill="x", padx=2, pady=(0, 2))

        self.txt_mtl_all_scratchpad = self._tag_role(
            tk.Text(
                pane,
                wrap="word",
                height=4,
                undo=True,
                font=("Segoe UI", 9),
                bg=t["bg_editor"],
                fg=editor_fg,
                insertbackground=t["misora_pink"],
                bd=1,
                relief="solid",
                padx=5,
                pady=4,
            ),
            "entry_editor",
        )
        self.txt_mtl_all_scratchpad.pack(fill="x", padx=2, pady=(0, 2))

        def _local_all_undo(_event=None):
            try:
                self.txt_mtl_all_scratchpad.edit_undo()
            except tk.TclError:
                pass
            return "break"

        def _local_all_redo(_event=None):
            try:
                self.txt_mtl_all_scratchpad.edit_redo()
            except tk.TclError:
                pass
            return "break"

        self.txt_mtl_all_scratchpad.bind("<Control-z>", _local_all_undo)
        self.txt_mtl_all_scratchpad.bind("<Control-Z>", _local_all_undo)
        self.txt_mtl_all_scratchpad.bind("<Control-y>", _local_all_redo)
        self.txt_mtl_all_scratchpad.bind("<Control-Y>", _local_all_redo)
        self.txt_mtl_all_scratchpad.bind("<Control-Shift-z>", _local_all_redo)
        self.txt_mtl_all_scratchpad.bind("<Control-Shift-Z>", _local_all_redo)

        self._apply_mtl_all_script_theme_tags()

    def _apply_mtl_all_script_theme_tags(self) -> None:
        """Configure the 5 static theme-aware status tags and block tags on All Script widgets."""
        if not hasattr(self, "txt_mtl_all_list") or not self.txt_mtl_all_list.winfo_exists():
            return
        t = self.theme
        editor_fg = best_contrast_fg(t["bg_editor"], t["fg_text"], "#ffffff")
        hl_fg = best_contrast_fg(t["highlight_bg"], t["fg_text"], "#ffffff")

        self.txt_mtl_all_list.configure(bg=t["bg_editor"], fg=editor_fg)
        self.txt_mtl_all_list.tag_configure("mtl_status_ready", foreground=t.get("accent_green", t["misora_pink"]), font=("Segoe UI", 9, "bold"))
        self.txt_mtl_all_list.tag_configure("mtl_status_translating", foreground=t.get("accent_blue", t["misora_pink"]), font=("Segoe UI", 9, "bold"))
        self.txt_mtl_all_list.tag_configure("mtl_status_error", foreground=t.get("accent_red", t["accent_yellow"]), font=("Segoe UI", 9, "bold"))
        self.txt_mtl_all_list.tag_configure("mtl_status_locked", foreground=t["fg_muted"], font=("Segoe UI", 9, "bold"))
        self.txt_mtl_all_list.tag_configure("mtl_status_empty", foreground=t["fg_muted"], font=("Segoe UI", 9))

        self.txt_mtl_all_list.tag_configure("mtl_block_header", foreground=t["misora_pink"], font=("Segoe UI", 9, "bold"))
        self.txt_mtl_all_list.tag_configure("mtl_block_src", foreground=t["fg_muted"], font=("Segoe UI", 8))
        self.txt_mtl_all_list.tag_configure("mtl_block_tr", foreground=editor_fg, font=("Segoe UI", 9))
        self.txt_mtl_all_list.tag_configure("mtl_block_selected", background=t["highlight_bg"], foreground=hl_fg)

        if hasattr(self, "txt_mtl_all_scratchpad") and self.txt_mtl_all_scratchpad.winfo_exists():
            self.txt_mtl_all_scratchpad.configure(bg=t["bg_editor"], fg=editor_fg, insertbackground=t["misora_pink"])

    def _set_mtl_drawer_mode(self, mode: str) -> None:
        if mode == "all_script":
            self._mtl_drawer_mode = "all_script"
            if hasattr(self, "btn_mtl_mode_dialogue"):
                self.btn_mtl_mode_dialogue.configure(style="TButton")
            if hasattr(self, "btn_mtl_mode_all_script"):
                self.btn_mtl_mode_all_script.configure(style="Pink.TButton")
            if hasattr(self, "btn_mtl_refresh_all") and self._is_widget_packed(self.btn_mtl_refresh_all):
                self.btn_mtl_refresh_all.pack_forget()
            for w_name in ("_mtl_dialogue_ctx_bar", "_mtl_dialogue_eng_bar", "_mtl_dialogue_wrap"):
                w = getattr(self, w_name, None)
                if w is not None and w.winfo_exists() and self._is_widget_packed(w):
                    w.pack_forget()
            body = getattr(self, "mtl_cards_body", None)
            if body is not None and body.winfo_exists():
                for child in list(body.winfo_children()):
                    child.destroy()
            if hasattr(self, "_mtl_drawer_cards") and isinstance(self._mtl_drawer_cards, dict):
                self._mtl_drawer_cards.clear()
            if hasattr(self, "mtl_all_script_frame") and self.mtl_all_script_frame.winfo_exists():
                if not self._is_widget_packed(self.mtl_all_script_frame):
                    self.mtl_all_script_frame.pack(fill="both", expand=True, padx=4, pady=(0, 6))
            self._refresh_mtl_drawer_box()
            return

        self._flush_mtl_all_scratchpad()
        self._mtl_drawer_mode = "dialogue"
        if hasattr(self, "btn_mtl_mode_dialogue"):
            self.btn_mtl_mode_dialogue.configure(style="Pink.TButton")
        if hasattr(self, "btn_mtl_mode_all_script"):
            self.btn_mtl_mode_all_script.configure(style="TButton")
        if hasattr(self, "mtl_all_script_frame") and self.mtl_all_script_frame.winfo_exists():
            if self._is_widget_packed(self.mtl_all_script_frame):
                self.mtl_all_script_frame.pack_forget()
        if hasattr(self, "btn_mtl_refresh_all") and not self._is_widget_packed(self.btn_mtl_refresh_all):
            self.btn_mtl_refresh_all.pack(side="right")
        if hasattr(self, "_mtl_dialogue_ctx_bar") and not self._is_widget_packed(self._mtl_dialogue_ctx_bar):
            self._mtl_dialogue_ctx_bar.pack(fill="x", padx=6, pady=(0, 4))
        if hasattr(self, "_mtl_dialogue_eng_bar") and not self._is_widget_packed(self._mtl_dialogue_eng_bar):
            self._mtl_dialogue_eng_bar.pack(fill="x", padx=6, pady=(0, 4))
        if hasattr(self, "_mtl_dialogue_wrap") and not self._is_widget_packed(self._mtl_dialogue_wrap):
            self._mtl_dialogue_wrap.pack(fill="both", expand=True, padx=4, pady=(0, 6))
        self._rebuild_mtl_drawer_cards()

    def _set_mtl_drawer_engine_enabled(self, engine_name: str, enabled: bool) -> None:
        if engine_name not in self._MTL_DRAWER_ENGINE_ORDER:
            return
        self._mtl_drawer_enabled_engines[engine_name] = bool(enabled)
        if engine_name in self._mtl_drawer_engine_vars:
            self._mtl_drawer_engine_vars[engine_name].set(bool(enabled))
        self._rebuild_mtl_drawer_cards()

    def _on_mtl_drawer_engine_toggled(self, engine_name: str) -> None:
        var = self._mtl_drawer_engine_vars.get(engine_name)
        if var is not None:
            self._mtl_drawer_enabled_engines[engine_name] = bool(var.get())
        self._rebuild_mtl_drawer_cards()

    def _rebuild_mtl_drawer_cards(self) -> None:
        """Rebuild vertical card stack strictly for currently enabled engines."""
        body = getattr(self, "mtl_cards_body", None)
        if body is None or not body.winfo_exists():
            return
        for child in list(body.winfo_children()):
            child.destroy()
        self._mtl_drawer_cards.clear()

        t = self.theme
        editor_fg = best_contrast_fg(t["bg_editor"], t["fg_text"], "#ffffff")
        enabled_engines = [e for e in self._MTL_DRAWER_ENGINE_ORDER if self._mtl_drawer_enabled_engines.get(e, False)]

        if not enabled_engines:
            self._tag_role(
                tk.Label(
                    body,
                    text="No engines enabled. Enable an engine above to translate.",
                    bg=t["bg_panel"],
                    fg=t["fg_muted"],
                    wraplength=260,
                    justify="left",
                ),
                "label_muted",
            ).pack(fill="x", padx=8, pady=12)
            return

        for eng in enabled_engines:
            card = self._tag_role(
                tk.Frame(
                    body,
                    bg=t["bg_panel"],
                    bd=1,
                    relief="solid",
                    highlightbackground=t["border"],
                    highlightthickness=1,
                ),
                "panel_box",
            )
            card.pack(fill="x", padx=6, pady=4)

            card_hdr = self._tag_role(tk.Frame(card, bg=t["bg_panel"]), "panel")
            card_hdr.pack(fill="x", padx=6, pady=(4, 2))

            self._tag_role(
                tk.Label(card_hdr, text=eng, bg=t["bg_panel"], fg=t["misora_pink"], anchor="w"),
                "label_accent",
            ).pack(side="left")

            lbl_status = self._tag_role(
                tk.Label(card_hdr, text="Ready", bg=t["bg_panel"], fg=t["fg_muted"], anchor="w"),
                "label_muted",
            )
            lbl_status.pack(side="left", padx=(6, 4), fill="x", expand=True)

            btn_apply = ttk.Button(
                card_hdr,
                text="→",
                style="Pink.TButton",
                width=3,
                command=lambda e=eng: self._on_mtl_drawer_apply_engine(e),
            )
            btn_apply.pack(side="right", padx=(2, 0))
            create_tooltip(btn_apply, f"Apply {eng} translation to active box (preserves whitespace)")

            btn_refresh = ttk.Button(
                card_hdr,
                text="↻",
                style="Small.TButton",
                width=3,
                command=lambda e=eng: self._on_mtl_drawer_refresh_engine(e),
            )
            btn_refresh.pack(side="right", padx=(2, 0))
            create_tooltip(btn_refresh, f"Refresh {eng} (bypass session cache)")

            scratch = self._tag_role(
                tk.Text(
                    card,
                    wrap="word",
                    height=3,
                    undo=True,
                    font=("Segoe UI", 9),
                    bg=t["bg_editor"],
                    fg=editor_fg,
                    insertbackground=t["misora_pink"],
                    bd=1,
                    relief="solid",
                    padx=5,
                    pady=4,
                ),
                "entry_editor",
            )
            scratch.pack(fill="x", padx=6, pady=(0, 6))

            # Isolate scratchpad from MisoraShortcuts and keep Ctrl+Z/Y strictly local
            def _local_undo(_event=None, w=scratch):
                try:
                    w.edit_undo()
                except tk.TclError:
                    pass
                return "break"

            def _local_redo(_event=None, w=scratch):
                try:
                    w.edit_redo()
                except tk.TclError:
                    pass
                return "break"

            scratch.bind("<Control-z>", _local_undo)
            scratch.bind("<Control-Z>", _local_undo)
            scratch.bind("<Control-y>", _local_redo)
            scratch.bind("<Control-Y>", _local_redo)
            scratch.bind("<Control-Shift-z>", _local_redo)
            scratch.bind("<Control-Shift-Z>", _local_redo)

            self._mtl_drawer_cards[eng] = {
                "frame": card,
                "lbl_status": lbl_status,
                "btn_refresh": btn_refresh,
                "btn_apply": btn_apply,
                "scratchpad": scratch,
            }

        self._mtl_drawer_active_context = None
        self._refresh_mtl_drawer_box()

    def _get_mtl_drawer_active_box(self) -> Optional[Tuple[int, Box]]:
        doc = getattr(self, "current_doc", None)
        if not doc or not doc.boxes or getattr(self, "is_box0_active", False):
            return None
        b_idx = getattr(self, "current_box_idx", 0)
        if b_idx < 0 or b_idx >= len(doc.boxes):
            return None
        return b_idx, doc.boxes[b_idx]

    def _refresh_mtl_drawer_box(self) -> None:
        """Sync MTL drawer box header, source preview, and cached scratchpads with active box."""
        if getattr(self, "_mtl_drawer_mode", "dialogue") == "all_script":
            if hasattr(self, "_refresh_mtl_all_script_view"):
                self._refresh_mtl_all_script_view()
            return
        if not hasattr(self, "lbl_mtl_box_info") or not self.lbl_mtl_box_info.winfo_exists():
            return
        active = self._get_mtl_drawer_active_box()
        if active is None:
            self._mtl_drawer_active_context = None
            if getattr(self, "is_box0_active", False) and self.current_doc:
                self.lbl_mtl_box_info.config(text=f"Box 0 / {len(self.current_doc.boxes)} (Metadata)")
                self.lbl_mtl_source_preview.config(text="Select a dialogue box to translate.")
            else:
                self.lbl_mtl_box_info.config(text="Box 0 / 0")
                self.lbl_mtl_source_preview.config(text="Open a story document to translate.")
            for card in self._mtl_drawer_cards.values():
                w = card["scratchpad"]
                if w.winfo_exists():
                    w.delete("1.0", tk.END)
                    w.edit_reset()
                if card["lbl_status"].winfo_exists():
                    card["lbl_status"].config(text="Ready")
            return

        b_idx, box = active
        total = len(self.current_doc.boxes)
        speaker = box.speaker or "(Narration)"
        self.lbl_mtl_box_info.config(text=f"Box {b_idx + 1} / {total} — {speaker}")
        preview = box.clean_text.replace("\n", " ")
        if len(preview) > 140:
            preview = preview[:137] + "..."
        self.lbl_mtl_source_preview.config(text=preview or "(Empty dialogue)")

        src_hash = _hash_mtl_source(box.clean_text)
        new_ctx = (str(self.current_file_path or ""), id(self.current_doc), _get_box_uid(box), src_hash)
        if new_ctx == getattr(self, "_mtl_drawer_active_context", None):
            return
        self._mtl_drawer_active_context = new_ctx

        for eng, card in self._mtl_drawer_cards.items():
            w = card["scratchpad"]
            lbl = card["lbl_status"]
            if not w.winfo_exists():
                continue
            cache_key = (eng, src_hash)
            w.delete("1.0", tk.END)
            if cache_key in self._mtl_drawer_cache:
                self._mtl_drawer_cache.move_to_end(cache_key)
                w.insert("1.0", self._mtl_drawer_cache[cache_key])
                if lbl.winfo_exists():
                    lbl.config(text="Cached")
            else:
                if lbl.winfo_exists():
                    lbl.config(text="Ready")
            w.edit_reset()

    def _mtl_drawer_cache_put(self, engine_name: str, src_hash: str, result: str) -> None:
        key = (engine_name, src_hash)
        self._mtl_drawer_cache[key] = result
        self._mtl_drawer_cache.move_to_end(key)
        while len(self._mtl_drawer_cache) > self._MTL_DRAWER_CACHE_MAX:
            self._mtl_drawer_cache.popitem(last=False)

    def _on_mtl_drawer_refresh_all(self) -> None:
        """Refresh all enabled engines for active box, using cache and confirming paid APIs."""
        active = self._get_mtl_drawer_active_box()
        if active is None:
            self.show_toast("Select a dialogue box to translate.")
            return
        _b_idx, box = active
        orig_text = box.clean_text
        if not orig_text.strip():
            self.show_toast("Current box has no text to translate.")
            return

        src_hash = _hash_mtl_source(orig_text)
        enabled = [e for e in self._MTL_DRAWER_ENGINE_ORDER if self._mtl_drawer_enabled_engines.get(e, False)]
        if not enabled:
            self.show_toast("No MTL engines enabled.")
            return

        paid_uncached = [
            e for e in enabled
            if e in self._MTL_DRAWER_PAID_ENGINES and (e, src_hash) not in self._mtl_drawer_cache
        ]
        allow_paid = True
        if paid_uncached:
            allow_paid = bool(
                messagebox.askyesno(
                    "Confirm Paid API Batch Call",
                    f"Refresh All will call paid API(s): {', '.join(paid_uncached)}.\n\nContinue?",
                    parent=self,
                )
            )

        for eng in enabled:
            if eng in self._MTL_DRAWER_PAID_ENGINES and (eng, src_hash) not in self._mtl_drawer_cache and not allow_paid:
                card = self._mtl_drawer_cards.get(eng)
                if card and card["lbl_status"].winfo_exists():
                    card["lbl_status"].config(text="Skipped (paid)")
                continue
            self._dispatch_mtl_drawer_engine(eng, bypass_cache=False)

    def _on_mtl_drawer_refresh_engine(self, engine_name: str) -> None:
        """Per-card Refresh: bypasses session cache for the specified engine."""
        self._dispatch_mtl_drawer_engine(engine_name, bypass_cache=True)

    def _dispatch_mtl_drawer_engine(self, engine_name: str, bypass_cache: bool = False) -> None:
        active = self._get_mtl_drawer_active_box()
        if active is None:
            self.show_toast("Select a dialogue box to translate.")
            return
        _b_idx, box = active
        orig_text = box.clean_text
        if not orig_text.strip():
            self.show_toast("Current box has no text to translate.")
            return

        src_hash = _hash_mtl_source(orig_text)
        card = self._mtl_drawer_cards.get(engine_name)

        if not bypass_cache and (engine_name, src_hash) in self._mtl_drawer_cache:
            self._mtl_drawer_cache.move_to_end((engine_name, src_hash))
            cached_val = self._mtl_drawer_cache[(engine_name, src_hash)]
            if card:
                if card["scratchpad"].winfo_exists():
                    card["scratchpad"].delete("1.0", tk.END)
                    card["scratchpad"].insert("1.0", cached_val)
                    card["scratchpad"].edit_reset()
                if card["lbl_status"].winfo_exists():
                    card["lbl_status"].config(text="Cached")
            return

        if card and card["lbl_status"].winfo_exists():
            card["lbl_status"].config(text="Translating...")

        self._mtl_drawer_req_seq += 1
        req_seq = self._mtl_drawer_req_seq
        self._mtl_drawer_latest_seq[engine_name] = req_seq

        cfg = MTLConfig.from_dict(self.mtl_config.to_dict())
        cfg.active_engine = engine_name
        cfg.protect_tags = True

        req_meta = (
            str(self.current_file_path or ""),
            id(self.current_doc),
            _get_box_uid(box),
            src_hash,
            req_seq,
            engine_name,
        )

        self._mtl_drawer_pending += 1
        translate_async(
            orig_text,
            cfg,
            out_queue=self._mtl_drawer_queue,
            metadata=req_meta,
            xuat_cache=getattr(self, "xuat_entries", None),
        )
        if self._mtl_drawer_poll_id is None and self.winfo_exists():
            self._mtl_drawer_poll_id = self.after(50, self._poll_mtl_drawer_queue)

    def _poll_mtl_drawer_queue(self) -> None:
        """Poll MTL drawer worker results on the Tk main thread (BUG-27, Rule 15)."""
        self._mtl_drawer_poll_id = None
        if not self.winfo_exists() or getattr(self, "_destroyed", False):
            return

        try:
            while True:
                msg = self._mtl_drawer_queue.get_nowait()
                self._mtl_drawer_pending = max(0, self._mtl_drawer_pending - 1)
                if not isinstance(msg, tuple) or len(msg) < 3:
                    continue
                kind, req_meta, payload = msg[0], msg[1], msg[2]
                if not isinstance(req_meta, tuple) or len(req_meta) < 6:
                    continue
                file_p, doc_id, b_uid, src_hash, req_seq, eng = req_meta[:6]
                mode_tag = req_meta[6] if len(req_meta) >= 7 else "dialogue"

                # Stale identity guard: discard if document or path changed
                if not self.current_doc or id(self.current_doc) != doc_id:
                    continue
                if str(self.current_file_path or "") != file_p:
                    continue

                if mode_tag == "all_script":
                    target_box = None
                    for b in self.current_doc.boxes:
                        if _get_box_uid(b) == b_uid:
                            target_box = b
                            break
                    if target_box is None:
                        continue
                    if _hash_mtl_source(target_box.clean_text) != src_hash:
                        continue
                    if req_seq < self._mtl_all_req_seqs.get((b_uid, eng), 0):
                        continue

                    ctx_key = (file_p, doc_id, b_uid, eng)
                    if kind == "success":
                        self._mtl_drawer_cache_put(eng, src_hash, payload)
                        self._mtl_all_results[ctx_key] = payload
                        self._mtl_all_statuses[ctx_key] = "ready"
                        self._mtl_all_errors.pop(ctx_key, None)
                        if (
                            b_uid == getattr(self, "_mtl_all_selected_uid", None)
                            and hasattr(self, "var_mtl_all_engine")
                            and self.var_mtl_all_engine.get() == eng
                        ):
                            self._load_mtl_all_scratchpad(force_text=payload)
                    elif kind == "error":
                        self._mtl_all_statuses[ctx_key] = "error"
                        self._mtl_all_errors[ctx_key] = str(payload)
                    if getattr(self, "_mtl_drawer_mode", "dialogue") == "all_script":
                        self._refresh_mtl_all_script_view(preserve_scroll=True)
                    continue

                active = self._get_mtl_drawer_active_box()
                if active is None:
                    continue
                _b_idx, curr_box = active
                if _get_box_uid(curr_box) != b_uid:
                    continue
                if _hash_mtl_source(curr_box.clean_text) != src_hash:
                    continue
                if req_seq < self._mtl_drawer_latest_seq.get(eng, 0):
                    continue

                card = self._mtl_drawer_cards.get(eng)
                if kind == "success":
                    self._mtl_drawer_cache_put(eng, src_hash, payload)
                    if card:
                        if card["scratchpad"].winfo_exists():
                            card["scratchpad"].delete("1.0", tk.END)
                            card["scratchpad"].insert("1.0", payload)
                            card["scratchpad"].edit_reset()
                        if card["lbl_status"].winfo_exists():
                            card["lbl_status"].config(text="✓ Ready")
                elif kind == "error":
                    if card and card["lbl_status"].winfo_exists():
                        card["lbl_status"].config(text=f"Error: {str(payload)[:40]}")
        except queue.Empty:
            pass

        if self._mtl_drawer_pending > 0 and self.winfo_exists() and not getattr(self, "_destroyed", False):
            self._mtl_drawer_poll_id = self.after(50, self._poll_mtl_drawer_queue)

    def _on_mtl_drawer_apply_engine(self, engine_name: str) -> bool:
        """Apply a card's scratchpad text to the active box (enforces lock, preserves whitespace)."""
        active = self._get_mtl_drawer_active_box()
        if active is None:
            self.show_toast("Select a dialogue box before applying translation.")
            return False
        b_idx, old_box = active

        if self.is_box_locked(b_idx):
            self.show_toast(f"🔒 Box {b_idx + 1} is locked against translation.")
            if hasattr(self, "lbl_status") and self.lbl_status.winfo_exists():
                self.lbl_status.config(text=f"Box {b_idx + 1} is locked against translation.")
            return False

        card = self._mtl_drawer_cards.get(engine_name)
        if not card or not card["scratchpad"].winfo_exists():
            return False

        new_text = card["scratchpad"].get("1.0", "end-1c")
        old_sp = old_box.speaker
        old_tx = old_box.clean_text
        box_uid = _get_box_uid(old_box)
        old_segs = [s.text for s in old_box.segs]

        try:
            self.current_doc.inject_box(b_idx, old_sp, new_text)
        except Exception as exc:
            self.logger.exception(f"MTL drawer apply failed for box {b_idx}:", exc)
            self.set_status(f"Error applying translation to Box #{b_idx + 1}: {exc}", is_error=True)
            return False

        new_segs = [s.text for s in self.current_doc.boxes[b_idx].segs]
        self.undo_journal.record(
            BoxEditDelta(
                box_index=b_idx,
                old_speaker=old_sp,
                new_speaker=old_sp,
                old_text=old_tx,
                new_text=new_text,
                file_path=str(self.current_file_path) if self.current_file_path else "",
                box_uid=box_uid,
                source="mtl",
                old_seg_texts=old_segs,
                new_seg_texts=new_segs,
            )
        )
        self._modified_boxes.add(b_idx)
        self._mark_document_dirty(self.current_file_path)
        self._dirty_state_changed()
        self._update_views()
        self.show_toast(f"✓ Applied {engine_name} translation to Box {b_idx + 1}")
        return True

    # -------------------------------------------------------------------------
    # Docked Right-Side MTL Drawer — All Script Mode Helpers (FEAT-13)
    # -------------------------------------------------------------------------
    @staticmethod
    def _is_mtl_empty_or_punct(text: str) -> bool:
        """Return True if text is empty or contains only whitespace/punctuation."""
        if not text or not text.strip():
            return True
        for ch in text:
            if ch.isalnum():
                return False
        return True

    def _mtl_all_ctx_key(self, box_uid: Any, engine_name: Optional[str] = None) -> Tuple[str, int, Any, str]:
        eng = engine_name or (self.var_mtl_all_engine.get() if hasattr(self, "var_mtl_all_engine") else "Google")
        return (str(self.current_file_path or ""), id(self.current_doc), box_uid, eng)

    def _find_box_index_by_uid(self, box_uid: Any) -> Optional[Tuple[int, Box]]:
        doc = getattr(self, "current_doc", None)
        if not doc or not doc.boxes:
            return None
        for idx, b in enumerate(doc.boxes):
            if _get_box_uid(b) == box_uid:
                return idx, b
        return None

    def _flush_mtl_all_scratchpad(self) -> None:
        """Persist current scratchpad text into document-scoped in-memory map before switching/applying."""
        if not hasattr(self, "txt_mtl_all_scratchpad") or not self.txt_mtl_all_scratchpad.winfo_exists():
            return
        last_ctx = getattr(self, "_mtl_all_last_ctx", None)
        if last_ctx is None:
            return
        _fp, doc_id, b_uid, eng = last_ctx
        if not self.current_doc or id(self.current_doc) != doc_id or b_uid is None:
            return
        text = self.txt_mtl_all_scratchpad.get("1.0", "end-1c")
        if last_ctx in self._mtl_all_results or text != "":
            self._mtl_all_results[last_ctx] = text
            if self._mtl_all_statuses.get(last_ctx) not in ("locked", "translating"):
                if text != "":
                    self._mtl_all_statuses[last_ctx] = "ready"

    def _load_mtl_all_scratchpad(self, force_text: Optional[str] = None) -> None:
        """Load selected box's translation into the shared bottom scratchpad."""
        if not hasattr(self, "txt_mtl_all_scratchpad") or not self.txt_mtl_all_scratchpad.winfo_exists():
            return
        doc = getattr(self, "current_doc", None)
        b_uid = getattr(self, "_mtl_all_selected_uid", None)
        eng = self.var_mtl_all_engine.get() if hasattr(self, "var_mtl_all_engine") else "Google"

        if not doc or not doc.boxes or b_uid is None:
            self._mtl_all_last_ctx = None
            if hasattr(self, "lbl_mtl_all_scratch_hdr") and self.lbl_mtl_all_scratch_hdr.winfo_exists():
                self.lbl_mtl_all_scratch_hdr.config(text="Scratchpad (No box selected)")
            self.txt_mtl_all_scratchpad.delete("1.0", tk.END)
            self.txt_mtl_all_scratchpad.edit_reset()
            return

        found = self._find_box_index_by_uid(b_uid)
        if found is None:
            self._mtl_all_last_ctx = None
            self.txt_mtl_all_scratchpad.delete("1.0", tk.END)
            self.txt_mtl_all_scratchpad.edit_reset()
            return

        b_idx, box = found
        ctx = self._mtl_all_ctx_key(b_uid, eng)
        self._mtl_all_last_ctx = ctx
        if hasattr(self, "lbl_mtl_all_scratch_hdr") and self.lbl_mtl_all_scratch_hdr.winfo_exists():
            sp = box.speaker or "(Narration)"
            self.lbl_mtl_all_scratch_hdr.config(text=f"Scratchpad — Box #{b_idx + 1} ({sp}) [{eng}]")

        if force_text is not None:
            val = force_text
        elif ctx in self._mtl_all_results:
            val = self._mtl_all_results[ctx]
        else:
            src_hash = _hash_mtl_source(box.clean_text)
            val = self._mtl_drawer_cache.get((eng, src_hash), "")

        self.txt_mtl_all_scratchpad.delete("1.0", tk.END)
        if val:
            self.txt_mtl_all_scratchpad.insert("1.0", val)
        self.txt_mtl_all_scratchpad.edit_reset()

    def _on_mtl_all_engine_changed(self, _event=None) -> None:
        self._flush_mtl_all_scratchpad()
        self._refresh_mtl_all_script_view()

    def _on_mtl_all_list_click(self, event: tk.Event) -> str:
        """Select clicked box block in txt_mtl_all_list and sync bottom scratchpad."""
        if not hasattr(self, "txt_mtl_all_list") or not self.txt_mtl_all_list.winfo_exists():
            return "break"
        try:
            idx_str = self.txt_mtl_all_list.index(f"@{event.x},{event.y}")
            clicked_line = int(idx_str.split(".")[0])
        except Exception:
            return "break"

        target_uid = None
        for start_l, end_l, b_uid in getattr(self, "_mtl_all_block_ranges", []):
            if start_l <= clicked_line <= end_l:
                target_uid = b_uid
                break

        if target_uid is not None and target_uid != self._mtl_all_selected_uid:
            self._flush_mtl_all_scratchpad()
            self._mtl_all_selected_uid = target_uid
            self._refresh_mtl_all_script_view(preserve_scroll=True)
        return "break"

    def _refresh_mtl_all_script_view(self, preserve_scroll: bool = False) -> None:
        """Render all boxes as non-truncated multi-line blocks in txt_mtl_all_list."""
        if not hasattr(self, "txt_mtl_all_list") or not self.txt_mtl_all_list.winfo_exists():
            return

        y_frac = 0.0
        if preserve_scroll:
            try:
                y_frac = self.txt_mtl_all_list.yview()[0]
            except Exception:
                y_frac = 0.0

        doc = getattr(self, "current_doc", None)
        eng = self.var_mtl_all_engine.get() if hasattr(self, "var_mtl_all_engine") else "Google"
        self._mtl_all_block_ranges = []

        self.txt_mtl_all_list.config(state="normal")
        try:
            self.txt_mtl_all_list.delete("1.0", tk.END)
            if not doc or not doc.boxes:
                msg = "Open a story document to translate." if not doc else "Story document has 0 dialogue boxes."
                self.txt_mtl_all_list.insert("1.0", msg, ("mtl_status_empty",))
                self._mtl_all_selected_uid = None
                self._load_mtl_all_scratchpad()
                return

            valid_uids = [_get_box_uid(b) for b in doc.boxes]
            if self._mtl_all_selected_uid not in valid_uids:
                active_idx = max(0, min(getattr(self, "current_box_idx", 0), len(doc.boxes) - 1))
                self._mtl_all_selected_uid = valid_uids[active_idx]

            status_meta = {
                "ready": ("✓", "mtl_status_ready"),
                "translating": ("⏳", "mtl_status_translating"),
                "error": ("⚠", "mtl_status_error"),
                "locked": ("🔒", "mtl_status_locked"),
                "empty": ("-", "mtl_status_empty"),
            }

            for idx, box in enumerate(doc.boxes):
                b_uid = valid_uids[idx]
                ctx = self._mtl_all_ctx_key(b_uid, eng)
                src_text = box.clean_text
                src_hash = _hash_mtl_source(src_text)

                if self.is_box_locked(idx):
                    st_key = "locked"
                elif ctx in self._mtl_all_statuses:
                    st_key = self._mtl_all_statuses[ctx]
                elif ctx in self._mtl_all_results or (eng, src_hash) in self._mtl_drawer_cache:
                    st_key = "ready"
                else:
                    st_key = "empty"

                icon, st_tag = status_meta.get(st_key, ("-", "mtl_status_empty"))
                start_line = int(self.txt_mtl_all_list.index("end-1c").split(".")[0])

                speaker = box.speaker or "(Narration)"
                self.txt_mtl_all_list.insert(tk.END, f"{icon} ", (st_tag,))
                hdr_tags = ("mtl_block_header", "mtl_block_selected") if b_uid == self._mtl_all_selected_uid else ("mtl_block_header",)
                self.txt_mtl_all_list.insert(tk.END, f"Box #{idx + 1} — {speaker}\n", hdr_tags)

                # Full multi-line JP source (no single-line truncation)
                self.txt_mtl_all_list.insert(tk.END, (src_text if src_text else "(Empty)") + "\n", ("mtl_block_src",))

                tr_val = self._mtl_all_results.get(ctx)
                if tr_val is None and st_key == "ready":
                    tr_val = self._mtl_drawer_cache.get((eng, src_hash))
                if tr_val:
                    self.txt_mtl_all_list.insert(tk.END, f"→ {tr_val}\n", ("mtl_block_tr",))
                elif st_key == "error":
                    err_msg = self._mtl_all_errors.get(ctx, "Translation failed")
                    self.txt_mtl_all_list.insert(tk.END, f"⚠ {err_msg}\n", ("mtl_status_error",))

                end_line = int(self.txt_mtl_all_list.index("end-1c").split(".")[0]) - 1
                self._mtl_all_block_ranges.append((start_line, max(start_line, end_line), b_uid))
                self.txt_mtl_all_list.insert(tk.END, "\n")

            if preserve_scroll:
                self.txt_mtl_all_list.yview_moveto(y_frac)
        finally:
            self.txt_mtl_all_list.config(state="disabled")

        self._load_mtl_all_scratchpad()

    def _dispatch_mtl_all_box(self, box_idx: int, box: Box, eng: str, bypass_cache: bool = False) -> bool:
        """Dispatch translate_async for a single box in All Script mode, returning True if worker started."""
        b_uid = _get_box_uid(box)
        ctx = self._mtl_all_ctx_key(b_uid, eng)
        orig_text = box.clean_text

        if self.is_box_locked(box_idx):
            self._mtl_all_statuses[ctx] = "locked"
            return False
        if self._is_mtl_empty_or_punct(orig_text):
            self._mtl_all_statuses[ctx] = "empty"
            return False

        src_hash = _hash_mtl_source(orig_text)
        if not bypass_cache and (eng, src_hash) in self._mtl_drawer_cache:
            self._mtl_drawer_cache.move_to_end((eng, src_hash))
            self._mtl_all_results[ctx] = self._mtl_drawer_cache[(eng, src_hash)]
            self._mtl_all_statuses[ctx] = "ready"
            return False

        self._mtl_all_statuses[ctx] = "translating"
        self._mtl_drawer_req_seq += 1
        req_seq = self._mtl_drawer_req_seq
        self._mtl_all_req_seqs[(b_uid, eng)] = req_seq

        cfg = MTLConfig.from_dict(self.mtl_config.to_dict())
        cfg.active_engine = eng
        cfg.protect_tags = True

        req_meta = (
            str(self.current_file_path or ""),
            id(self.current_doc),
            b_uid,
            src_hash,
            req_seq,
            eng,
            "all_script",
        )
        self._mtl_drawer_pending += 1
        translate_async(
            orig_text,
            cfg,
            out_queue=self._mtl_drawer_queue,
            metadata=req_meta,
            xuat_cache=getattr(self, "xuat_entries", None),
        )
        if self._mtl_drawer_poll_id is None and self.winfo_exists():
            self._mtl_drawer_poll_id = self.after(50, self._poll_mtl_drawer_queue)
        return True

    def _on_mtl_all_script_refresh_selected(self) -> None:
        """Refresh the currently selected box in All Script mode (bypasses session cache)."""
        doc = getattr(self, "current_doc", None)
        if not doc or not doc.boxes:
            self.show_toast("Open a story document to translate.")
            return
        found = self._find_box_index_by_uid(getattr(self, "_mtl_all_selected_uid", None))
        if found is None:
            self.show_toast("Select a box in the list to refresh.")
            return
        b_idx, box = found
        if self.is_box_locked(b_idx):
            self.show_toast(f"🔒 Box {b_idx + 1} is locked against translation.")
            return
        eng = self.var_mtl_all_engine.get()
        self._dispatch_mtl_all_box(b_idx, box, eng, bypass_cache=True)
        self._refresh_mtl_all_script_view(preserve_scroll=True)

    def _on_mtl_all_script_apply_selected(self) -> bool:
        """Apply scratchpad text to the selected box by box.uid (enforces lock, preserves whitespace)."""
        self._flush_mtl_all_scratchpad()
        doc = getattr(self, "current_doc", None)
        if not doc or not doc.boxes:
            self.show_toast("Open a story document first.")
            return False
        found = self._find_box_index_by_uid(getattr(self, "_mtl_all_selected_uid", None))
        if found is None:
            self.show_toast("Select a box before applying translation.")
            return False
        b_idx, old_box = found
        if self.is_box_locked(b_idx):
            self.show_toast(f"🔒 Box {b_idx + 1} is locked against translation.")
            return False

        new_text = self.txt_mtl_all_scratchpad.get("1.0", "end-1c")
        old_sp = old_box.speaker
        old_tx = old_box.clean_text
        box_uid = _get_box_uid(old_box)
        old_segs = [s.text for s in old_box.segs]

        try:
            doc.inject_box(b_idx, old_sp, new_text)
        except Exception as exc:
            self.logger.exception(f"All Script Apply Selected failed for box {b_idx}:", exc)
            self.set_status(f"Error applying translation to Box #{b_idx + 1}: {exc}", is_error=True)
            return False

        new_segs = [s.text for s in doc.boxes[b_idx].segs]
        self.undo_journal.record(
            BoxEditDelta(
                box_index=b_idx,
                old_speaker=old_sp,
                new_speaker=old_sp,
                old_text=old_tx,
                new_text=new_text,
                file_path=str(self.current_file_path) if self.current_file_path else "",
                box_uid=box_uid,
                source="mtl",
                old_seg_texts=old_segs,
                new_seg_texts=new_segs,
            )
        )
        self._modified_boxes.add(b_idx)
        self._mark_document_dirty(self.current_file_path)
        self._dirty_state_changed()
        self._update_views()
        self.show_toast(f"✓ Applied translation to Box {b_idx + 1}")
        return True

    def _on_mtl_all_script_translate_all(self) -> None:
        """Batch-translate all unlocked, non-empty boxes using the selected engine."""
        doc = getattr(self, "current_doc", None)
        if not doc or not doc.boxes:
            self.show_toast("Open a story document to translate.")
            return
        eng = self.var_mtl_all_engine.get()

        if eng in self._MTL_DRAWER_PAID_ENGINES:
            uncached_count = 0
            for idx, box in enumerate(doc.boxes):
                if self.is_box_locked(idx) or self._is_mtl_empty_or_punct(box.clean_text):
                    continue
                if (eng, _hash_mtl_source(box.clean_text)) not in self._mtl_drawer_cache:
                    uncached_count += 1
            if uncached_count > 0:
                ok = messagebox.askyesno(
                    "Confirm Paid API Batch Call",
                    f"Translate All will call paid API '{eng}' for {uncached_count} uncached box(es).\n\nContinue?",
                    parent=self,
                )
                if not ok:
                    return

        for idx, box in enumerate(doc.boxes):
            self._dispatch_mtl_all_box(idx, box, eng, bypass_cache=False)

        self._refresh_mtl_all_script_view(preserve_scroll=True)

    def _on_mtl_all_script_apply_all(self) -> int:
        """Apply all ready/edited translations to unlocked boxes in one Undo batch."""
        self._flush_mtl_all_scratchpad()
        doc = getattr(self, "current_doc", None)
        if not doc or not doc.boxes:
            self.show_toast("Open a story document first.")
            return 0
        eng = self.var_mtl_all_engine.get()

        candidates: List[Tuple[Any, str]] = []
        for idx, box in enumerate(doc.boxes):
            if self.is_box_locked(idx):
                continue
            b_uid = _get_box_uid(box)
            ctx = self._mtl_all_ctx_key(b_uid, eng)
            st = self._mtl_all_statuses.get(ctx)
            if st in ("locked", "translating", "error"):
                continue
            tr_text = self._mtl_all_results.get(ctx)
            if tr_text is None:
                src_hash = _hash_mtl_source(box.clean_text)
                if (eng, src_hash) in self._mtl_drawer_cache:
                    tr_text = self._mtl_drawer_cache[(eng, src_hash)]
            if tr_text is None or tr_text == "":
                continue
            candidates.append((b_uid, tr_text))

        if not candidates:
            self.show_toast("No ready translations to apply.")
            return 0

        applied_count = 0
        self.undo_journal.begin_batch("MTL Apply All")
        try:
            for b_uid, new_text in candidates:
                found = self._find_box_index_by_uid(b_uid)
                if found is None:
                    continue
                b_idx, old_box = found
                if self.is_box_locked(b_idx):
                    continue
                old_sp = old_box.speaker
                old_tx = old_box.clean_text
                old_segs = [s.text for s in old_box.segs]
                try:
                    doc.inject_box(b_idx, old_sp, new_text)
                except Exception as exc:
                    self.logger.exception(f"MTL Apply All failed for box {b_idx}:", exc)
                    continue
                new_segs = [s.text for s in doc.boxes[b_idx].segs]
                self.undo_journal.record(
                    BoxEditDelta(
                        box_index=b_idx,
                        old_speaker=old_sp,
                        new_speaker=old_sp,
                        old_text=old_tx,
                        new_text=new_text,
                        file_path=str(self.current_file_path) if self.current_file_path else "",
                        box_uid=b_uid,
                        source="mtl",
                        old_seg_texts=old_segs,
                        new_seg_texts=new_segs,
                    )
                )
                self._modified_boxes.add(b_idx)
                applied_count += 1
        finally:
            self.undo_journal.end_batch()

        if applied_count > 0:
            self._mark_document_dirty(self.current_file_path)
            self._dirty_state_changed()
            self._update_views()
            self.show_toast(f"✓ Applied {eng} translations to {applied_count} box(es)")
        else:
            self.show_toast("No translations were applied.")
        return applied_count

