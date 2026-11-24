# ======================================================================
# FILE: misora.py — PART 04 / 10
# ORIGINAL LINE RANGE : L3687 .. L5182 (total 1496 lines of 12835)
# SOURCE SHA-256      : d23baae2be82fe93a18da7d3769af30d19ebe02a8b5f6a3645d56a6f53c0710e
# NOTE FOR AI REVIEWER: Cite ORIGINAL line numbers (L3687..L5182) and symbol names.
# SYMBOLS IN THIS PART (with exact original line numbers):
#   L03687:   MisoraApp._build_main_panels (def)
#   L04868:   MisoraApp._on_debug_settings_changed (def)
#   L04881:   MisoraApp._sync_debug_menu_states (def)
#   L04889:   MisoraApp._on_open_debug_log_file (def)
#   L04901:   MisoraApp._on_clear_debug_log_file (def)
#   L04909:   MisoraApp._on_speaker_dropdown_clicked (def)
#   L04939:   MisoraApp._assign_speaker_to_current_box (def)
#   L04946:   MisoraApp._append_speaker_attribute (def)
#   L04953:   MisoraApp._prompt_append_speaker_attribute (def)
#   L04994:   MisoraApp._is_widget_packed (def)
#   L05001:   MisoraApp._on_toggle_line_numbers (def)
#   L05053:   MisoraApp._on_toggle_column_ruler (def)
#   L05083:   MisoraApp._update_gutter_clean (def)
#   L05097:   MisoraApp._update_gutter_cont (def)
#   L05109:   MisoraApp._sync_continuous_gutter_scroll (def)
#   L05117:   MisoraApp._on_continuous_vscroll (def)
#   L05126:   MisoraApp._highlight_secret_whitespace (def)
#   L05136:   MisoraApp._shortcut_wrap (def)
#   L05140:   MisoraApp._shortcut_undo (def)
#   L05144:   MisoraApp._shortcut_redo (def)
#   L05148:   MisoraApp._set_ribbon_colors (def)
#   L05159:   MisoraApp._apply_active_ribbon_color (def)
#   L05163:   MisoraApp._apply_active_ribbon_gradient (def)
#   L05168:   MisoraApp.on_open_color_picker (def)
# ======================================================================

    def _build_main_panels(self) -> None:
        t = self.theme
        d_fam = self.prefs["dialogue_font_family"]
        d_sz = int(self.prefs["dialogue_font_size"])
        r_sz = int(self.prefs["raw_font_size"])
        u_sz = int(self.prefs["ui_font_size"])

        self.h_paned = self._tag_role(
            tk.PanedWindow(
                self,
                orient=tk.HORIZONTAL,
                bg=t["border"],
                sashwidth=6,
                sashrelief="flat",
                opaqueresize=False
            ),
            "sash"
        )
        self.h_paned.pack(fill="both", expand=True, padx=8, pady=4)

        # LEFT PANEL: Upgraded Dual-Tab Dock (Search Results & Opened Files Cache #3B)
        self.left_frame = self._tag_role(tk.Frame(self.h_paned, bg=t["bg_panel"]), "panel")
        self.h_paned.add(self.left_frame, minsize=160, width=self._left_dock_width, stretch="never")

        # Dock Tab Switcher Bar
        self.dock_tab_bar = self._tag_role(tk.Frame(self.left_frame, bg=t["bg_panel"]), "panel")
        self.dock_tab_bar.pack(fill="x", padx=4, pady=(4, 2))

        self.btn_tab_search = tk.Button(
            self.dock_tab_bar,
            text="Search Results",
            font=("Segoe UI", max(8, u_sz - 1), "bold"),
            relief="flat",
            bd=1,
            cursor="hand2",
            command=lambda: self._switch_dock_tab("search"),
        )
        self.btn_tab_search.pack(side="left", padx=(2, 2))

        self.btn_tab_files = tk.Button(
            self.dock_tab_bar,
            text="Opened Files",
            font=("Segoe UI", max(8, u_sz - 1), "bold"),
            relief="flat",
            bd=1,
            cursor="hand2",
            command=lambda: self._switch_dock_tab("files"),
        )
        self.btn_tab_files.pack(side="left", padx=(2, 2))

        self.btn_dock_pin = ttk.Button(
            self.dock_tab_bar,
            text="📌",
            style="Small.TButton",
            command=self._toggle_dock_collapse,
            width=3,
        )
        self.btn_dock_pin.pack(side="right", padx=(2, 2))
        self._dock_pin_tooltip = create_tooltip(self.btn_dock_pin, "Collapse Left Panel")

        # --- TAB 1: Search Results ---
        self.tab_search_frame = self._tag_role(tk.Frame(self.left_frame, bg=t["bg_panel"]), "panel")

        left_header = self._tag_role(tk.Frame(self.tab_search_frame, bg=t["bg_panel"]), "panel")
        left_header.pack(fill="x", padx=6, pady=(4, 4))
        self.lbl_results_title = self._tag_role(
            tk.Label(
                left_header,
                text="Search Results (0 matches)",
                font=("Segoe UI", u_sz, "bold"),
                bg=t["bg_panel"],
                fg=t["misora_pink"],
                anchor="w"
            ),
            "label_accent"
        )
        self.lbl_results_title.pack(side="left", fill="x", expand=True)

        self.btn_clear_res = ttk.Button(left_header, text="Clear", style="Small.TButton", command=self.on_clear_search)
        self.btn_clear_res.pack(side="right")
        create_tooltip(self.btn_clear_res, "Clear Search Results")

        self.tree_container = self._tag_role(tk.Frame(self.tab_search_frame, bg=t["bg_editor"], bd=1, relief="solid"), "editor_box")
        self.tree_container.pack(fill="both", expand=True, padx=4, pady=(0, 6))
        self.tree_container.pack_propagate(False)

        res_scroll_y = tk.Scrollbar(self.tree_container, orient="vertical")
        res_scroll_y.pack(side="right", fill="y")
        res_scroll_x = tk.Scrollbar(self.tree_container, orient="horizontal")
        res_scroll_x.pack(side="bottom", fill="x")

        self.txt_results = tk.Text(
            self.tree_container,
            wrap="none",
            font=("Segoe UI", u_sz),
            bg=t["bg_editor"],
            fg=t["fg_text"],
            insertwidth=0,
            cursor="arrow",
            padx=6,
            pady=4,
            bd=0,
            relief="flat",
            exportselection=False,
            state="disabled",
            yscrollcommand=res_scroll_y.set,
            xscrollcommand=res_scroll_x.set,
        )
        self.txt_results.pack(side="left", fill="both", expand=True)
        res_scroll_y.config(command=self.txt_results.yview)
        res_scroll_x.config(command=self.txt_results.xview)

        self.txt_results.tag_configure(
            "file_header",
            font=("Segoe UI", u_sz, "bold"),
            foreground=t["misora_pink"],
            spacing1=4,
            spacing3=2,
        )
        self.txt_results.tag_configure(
            "box_badge",
            font=("Consolas", max(8, u_sz - 1), "bold"),
            foreground=t["accent_blue"],
        )
        self.txt_results.tag_configure(
            "speaker_tag",
            font=("Segoe UI", u_sz, "bold"),
            foreground=t["fg_text"],
        )
        self.txt_results.tag_configure(
            "selected_row",
            background=t["highlight_bg"],
        )
        self.txt_results.tag_configure(
            "match_hl",
            background=t["misora_pink"],
            foreground=best_contrast_fg(t["misora_pink"]),
            font=("Segoe UI", u_sz, "bold"),
        )
        self.txt_results.tag_raise("match_hl")

        self.txt_results.bind("<Button-1>", self._on_results_click)
        self.txt_results.bind("<Button-3>", self._on_results_right_click)
        self.txt_results.bind("<Up>", lambda e: self._on_results_step(-1))
        self.txt_results.bind("<Down>", lambda e: self._on_results_step(1))

        # --- TAB 2: Opened Files Cache ---
        self.tab_files_frame = self._tag_role(tk.Frame(self.left_frame, bg=t["bg_panel"]), "panel")

        files_header = self._tag_role(tk.Frame(self.tab_files_frame, bg=t["bg_panel"]), "panel")
        files_header.pack(fill="x", padx=6, pady=(4, 4))
        self.lbl_files_title = self._tag_role(
            tk.Label(
                files_header,
                text="Opened Files (0)",
                font=("Segoe UI", u_sz, "bold"),
                bg=t["bg_panel"],
                fg=t["misora_pink"],
                anchor="w"
            ),
            "label_accent"
        )
        self.lbl_files_title.pack(side="left", fill="x", expand=True)

        self.ico_folder = self.get_icon("folder", (13, 13))
        btn_open_more = ttk.Button(files_header, text=" Open...", image=self.ico_folder, compound="left", style="Small.TButton", command=self.on_open_file)
        btn_open_more.pack(side="right")

        self.files_container = self._tag_role(tk.Frame(self.tab_files_frame, bg=t["bg_editor"], bd=1, relief="solid"), "editor_box")
        self.files_container.pack(fill="both", expand=True, padx=4, pady=(0, 6))
        self.files_container.pack_propagate(False)

        files_scroll_y = tk.Scrollbar(self.files_container, orient="vertical")
        files_scroll_y.pack(side="right", fill="y")
        files_scroll_x = tk.Scrollbar(self.files_container, orient="horizontal")
        files_scroll_x.pack(side="bottom", fill="x")

        self.txt_opened_files = tk.Text(
            self.files_container,
            wrap="none",
            font=("Segoe UI", u_sz),
            bg=t["bg_editor"],
            fg=t["fg_text"],
            insertwidth=0,
            cursor="arrow",
            padx=6,
            pady=4,
            bd=0,
            relief="flat",
            exportselection=False,
            state="disabled",
            yscrollcommand=files_scroll_y.set,
            xscrollcommand=files_scroll_x.set,
        )
        self.txt_opened_files.pack(side="left", fill="both", expand=True)
        files_scroll_y.config(command=self.txt_opened_files.yview)
        files_scroll_x.config(command=self.txt_opened_files.xview)

        self.txt_opened_files.tag_configure("file_active", font=("Segoe UI", u_sz, "bold"), foreground=t["misora_pink"], background=t["highlight_bg"])
        self.txt_opened_files.tag_configure("file_dirty", font=("Segoe UI", u_sz, "bold"), foreground=t["accent_yellow"])
        self.txt_opened_files.tag_configure("file_normal", font=("Segoe UI", u_sz), foreground=t["fg_text"])
        self.txt_opened_files.tag_configure("file_dim", font=("Segoe UI", max(8, u_sz - 1)), foreground=t["fg_muted"])
        self.txt_opened_files.tag_configure("file_close", font=("Consolas", max(8, u_sz - 1), "bold"), foreground=t["misora_pink"])

        self.txt_opened_files.bind("<Button-1>", self._on_opened_files_click)
        self.txt_opened_files.bind("<Button-3>", self._on_opened_files_right_click)

        # Show initial dock tab
        self._switch_dock_tab(self._left_dock_tab)

        # CENTER PANEL: Dual-View Editor (Vertical Splitter)
        right_frame = self._tag_role(tk.Frame(self.h_paned, bg=t["bg_panel"]), "panel")
        self.h_paned.add(right_frame, minsize=420, stretch="always")

        self.v_paned = self._tag_role(
            tk.PanedWindow(
                right_frame,
                orient=tk.VERTICAL,
                bg=t["border"],
                sashwidth=6,
                sashrelief="flat",
                opaqueresize=True
            ),
            "sash"
        )
        self.v_paned.pack(fill="both", expand=True)

        # TOP VIEW: Game Display View (Page-by-Page OR Continuous Dialog Stream)
        top_view = self._tag_role(tk.Frame(self.v_paned, bg=t["bg_panel"]), "panel")
        self.v_paned.add(top_view, minsize=140, height=400, stretch="always")

        gd_header = self._tag_role(tk.Frame(top_view, bg=t["bg_panel"]), "panel")
        gd_header.pack(fill="x", padx=8, pady=(4, 2))

        self.lbl_gd_title = self._tag_role(
            tk.Label(
                gd_header,
                text="GAME VIEW (Clean Dialogue)",
                font=("Segoe UI", u_sz, "bold"),
                bg=t["bg_panel"],
                fg=t["misora_pink"]
            ),
            "label_accent"
        )
        self.lbl_gd_title.pack(side="left")

        self.lbl_box_counter = self._tag_role(
            tk.Label(gd_header, text="Box: 0 / 0", font=("Segoe UI", u_sz), bg=t["bg_panel"], fg=t["fg_muted"]),
            "label_muted"
        )
        self.lbl_box_counter.pack(side="right", padx=(6, 0))

        self.ico_next = self.get_icon("nav_next", (14, 14))
        self.btn_next = ttk.Button(gd_header, text="Next ", image=self.ico_next, compound="right", style="Nav.TButton", command=self.on_next_box)
        self.btn_next.pack(side="right", padx=(2, 0))

        self.ico_prev = self.get_icon("nav_prev", (14, 14))
        self.btn_prev = ttk.Button(gd_header, text=" Prev", image=self.ico_prev, compound="left", style="Nav.TButton", command=self.on_prev_box)
        self.btn_prev.pack(side="right", padx=(4, 2))

        self.ico_ai = self.get_icon("ai", (16, 16))
        btn_ai_prompt = ttk.Button(gd_header, text=" AI Prompt", image=self.ico_ai, compound="left", style="Small.TButton", command=self.on_copy_ai_prompt)
        btn_ai_prompt.pack(side="right", padx=(4, 2))

        self.ico_mtl = self.get_icon("mtl", (16, 16))
        btn_translate = ttk.Button(gd_header, text=" MTL", image=self.ico_mtl, compound="left", style="Small.TButton", command=self.on_open_translator_assistant)
        btn_translate.pack(side="right", padx=(2, 2))

        cb_cont = ttk.Checkbutton(
            gd_header,
            text="Continuous View",
            variable=self.var_continuous_view,
            command=self._on_toggle_continuous_view,
            style="Accent.TCheckbutton",
            cursor="hand2"
        )
        cb_cont.pack(side="right", padx=(4, 4))

        cb_sel_box = ttk.Checkbutton(
            gd_header,
            text="Select Box",
            variable=self.var_select_box_mode,
            command=self._on_toggle_select_box_mode,
            style="Accent.TCheckbutton",
            cursor="hand2"
        )
        cb_sel_box.pack(side="right", padx=(4, 4))

        # Combined Row for Speaker + Compact NGUI Ribbon (#7 & #10)
        speaker_ribbon_row = self._tag_role(tk.Frame(top_view, bg=t["bg_panel"]), "panel")
        speaker_ribbon_row.pack(fill="x", padx=8, pady=(2, 4))

        self._tag_role(
            tk.Label(speaker_ribbon_row, text="Speaker:", bg=t["bg_panel"], fg=t["fg_muted"]),
            "label_muted"
        ).pack(side="left", padx=(0, 4))

        self.speaker_var = tk.StringVar(master=self)
        self.entry_speaker = self._tag_role(
            tk.Entry(
                speaker_ribbon_row,
                textvariable=self.speaker_var,
                font=(d_fam, max(9, d_sz - 1), "bold"),
                bg=t["bg_editor"],
                fg=t["fg_text"],
                insertbackground=t["misora_pink"],
                selectbackground=t["highlight_bg"],
                selectforeground=t["misora_pink"],
                bd=1,
                relief="solid",
                width=14
            ),
            "entry_speaker"
        )
        self.entry_speaker.pack(side="left")
        self.entry_speaker.bind("<KeyRelease>", lambda e: self._on_speaker_edited())
        self.entry_speaker.bind("<<Cut>>", lambda e: self.after_idle(self._commit_speaker_edit))
        self.entry_speaker.bind("<<Paste>>", lambda e: self.after_idle(self._commit_speaker_edit))

        self.btn_speaker_dropdown = ttk.Button(
            speaker_ribbon_row,
            text="▼",
            style="Small.TButton",
            width=2,
            command=self._on_speaker_dropdown_clicked,
        )
        self.btn_speaker_dropdown.pack(side="left", padx=(2, 2))
        create_tooltip(self.btn_speaker_dropdown, "Select Speaker from Recent List")

        self.ico_pin = self.get_icon("pin", (16, 16))
        self.btn_pin_speaker = tk.Button(
            speaker_ribbon_row,
            text="📌",
            image=self.ico_pin,
            fg=t["fg_text"],
            bg=t["bg_panel"],
            activebackground=t["highlight_bg"],
            activeforeground=t["fg_text"],
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self._on_toggle_pin_speaker,
        )
        self.btn_pin_speaker.pack(side="left", padx=(1, 4))
        create_tooltip(self.btn_pin_speaker, "Pin Speaker (locks current speaker across box navigation)")

        self.lbl_voice_cue = self._tag_role(
            tk.Label(speaker_ribbon_row, text="", bg=t["bg_panel"], fg=t["accent_blue"], font=("Segoe UI", max(8, u_sz - 1))),
            "label_voice"
        )
        self.lbl_voice_cue.pack(side="left", padx=(2, 4))

        self.lbl_segs_badge = self._tag_role(
            tk.Label(speaker_ribbon_row, text="", bg=t["bg_panel"], fg=t["misora_pink"], font=("Segoe UI", max(7, u_sz - 2), "bold")),
            "label_accent"
        )
        self.lbl_segs_badge.pack(side="left", padx=(2, 4))

        # Translation Lock Toggle Button (Rule 20 D8 / TRANSLATION-LOCK)
        self.btn_lock_box = tk.Button(
            speaker_ribbon_row,
            text="🔓",
            font=("Segoe UI", max(8, u_sz - 1)),
            bg=t["bg_panel"],
            activebackground=t["highlight_bg"],
            bd=1,
            relief="solid",
            cursor="hand2",
            command=self.on_toggle_lock_current_box,
            padx=3,
            pady=0,
        )
        self.btn_lock_box.pack(side="left", padx=(2, 4))
        create_tooltip(self.btn_lock_box, "Translation Lock (Ctrl+L) — Protect box from batch/paste/replace")

        # Rendered Character Count & Game Box Overflow Warning (Rule 19, Rule 20 D13 / GAME-BOX-PREVIEW)
        self.lbl_char_count = self._tag_role(
            tk.Label(speaker_ribbon_row, text="", bg=t["bg_panel"], fg=t["fg_muted"], font=("Segoe UI", max(8, u_sz - 1))),
            "label_char_count"
        )
        self.lbl_char_count.pack(side="left", padx=(2, 6))
        create_tooltip(self.lbl_char_count, "Rendered dialogue length (excluding NGUI tags). Warns on overflow (>45 chars/line).")

        # Compact NGUI Ribbon docked on the right side of the Speaker row
        dark_p = self._is_dark_color(t["bg_panel"])
        btn_bg = self._shift_hex(t["bg_panel"], 10 if dark_p else -8)
        btn_hover = self._shift_hex(t["bg_panel"], 22 if dark_p else -16)
        btn_fg = best_contrast_fg(btn_bg, t["fg_text"], "#ffffff")
        accent_bg = t["misora_pink"]
        accent_hover = t["misora_pink_hover"]
        fg_accent = best_contrast_fg(accent_bg)
        accent_green = t.get("accent_green", "#2e7d32")

        ribbon = self._tag_role(
            tk.Frame(speaker_ribbon_row, bg=t["bg_editor"], bd=1, relief="solid", highlightbackground=t["border"], highlightthickness=1),
            "ribbon"
        )
        ribbon.pack(side="right", padx=(4, 0))

        self.btn_ribbon_swatch = tk.Button(
            ribbon,
            width=2,
            bg=self._active_ngui_color,
            activebackground=self._active_ngui_color,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self.on_open_color_picker,
        )
        self.btn_ribbon_swatch.pack(side="left", padx=(2, 1), pady=1)
        create_tooltip(self.btn_ribbon_swatch, "Active NGUI Color (Click to open Color Picker)")

        self.ico_palette = self.get_icon("palette", (16, 16))
        btn_color = self._tag_role(
            tk.Button(
                ribbon,
                text=" Color",
                image=self.ico_palette,
                compound="left",
                font=("Segoe UI", 8, "bold"),
                bg=accent_bg,
                fg=fg_accent,
                activebackground=accent_hover,
                activeforeground=fg_accent,
                bd=1,
                relief="raised",
                padx=3,
                pady=0,
                cursor="hand2",
                command=self._apply_active_ribbon_color,
            ),
            "ribbon_primary_btn",
        )
        btn_color.pack(side="left", padx=1, pady=1)
        create_tooltip(btn_color, "Apply hex color tag [RRGGBB]")

        btn_grad = self._tag_role(
            tk.Button(
                ribbon,
                text="Grad",
                font=("Segoe UI", 8, "bold"),
                bg=accent_bg,
                fg=fg_accent,
                activebackground=accent_hover,
                activeforeground=fg_accent,
                bd=1,
                relief="raised",
                padx=3,
                pady=0,
                cursor="hand2",
                command=self._apply_active_ribbon_gradient,
            ),
            "ribbon_primary_btn",
        )
        btn_grad.pack(side="left", padx=1, pady=1)
        create_tooltip(btn_grad, "Apply vertical gradient tag [top-bottom]")

        self.ico_eyedropper = self.get_icon("eyedropper", (16, 16))
        self.btn_eyedropper = self._tag_role(
            tk.Button(
                ribbon,
                text="🎨",
                image=self.ico_eyedropper,
                fg=btn_fg,
                bg=btn_bg,
                activebackground=btn_hover,
                activeforeground=btn_fg,
                bd=1,
                relief="raised",
                cursor="hand2",
                command=self.on_open_color_picker,
            ),
            "ribbon_btn",
        )
        self.btn_eyedropper.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_eyedropper, "Open NGUI Color & Gradient Picker")

        # Text & Box Actions Toolbar (docked in speaker row next to formatting ribbon)
        actions_bar = self._tag_role(
            tk.Frame(speaker_ribbon_row, bg=t["bg_editor"], bd=1, relief="solid", highlightbackground=t["border"], highlightthickness=1),
            "actions_toolbar"
        )
        actions_bar.pack(side="right", padx=(2, 4))

        # Text Actions Group (Select Whole Story, Cut, Copy, Paste)
        self.ico_sel_story = self.get_icon("select_story", (16, 16))
        self.btn_sel_story = self._tag_role(
            tk.Button(actions_bar, text="🗎", image=self.ico_sel_story, fg=btn_fg, bg=btn_bg, activebackground=btn_hover, activeforeground=btn_fg, bd=1, relief="raised", cursor="hand2", command=self.on_select_whole_story),
            "ribbon_btn"
        )
        self.btn_sel_story.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_sel_story, "Select Whole Story Dialogue (Ctrl+Alt+A)")

        self.ico_cut = self.get_icon("cut", (16, 16))
        self.btn_cut = self._tag_role(
            tk.Button(actions_bar, text="✂", image=self.ico_cut, fg=btn_fg, bg=btn_bg, activebackground=btn_hover, activeforeground=btn_fg, bd=1, relief="raised", cursor="hand2", command=self.on_text_cut),
            "ribbon_btn"
        )
        self.btn_cut.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_cut, "Cut Text (Ctrl+X)")

        self.ico_copy = self.get_icon("copy", (16, 16))
        self.btn_copy = self._tag_role(
            tk.Button(actions_bar, text="📋", image=self.ico_copy, fg=btn_fg, bg=btn_bg, activebackground=btn_hover, activeforeground=btn_fg, bd=1, relief="raised", cursor="hand2", command=self.on_text_copy),
            "ribbon_btn"
        )
        self.btn_copy.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_copy, "Copy Text (Ctrl+C)")

        self.ico_paste = self.get_icon("paste", (16, 16))
        self.btn_paste = self._tag_role(
            tk.Button(actions_bar, text="📥", image=self.ico_paste, fg=btn_fg, bg=btn_bg, activebackground=btn_hover, activeforeground=btn_fg, bd=1, relief="raised", cursor="hand2", command=self.on_text_paste),
            "ribbon_btn"
        )
        self.btn_paste.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_paste, "Paste Text / Multi-Box Delimiter Split (Ctrl+V)")

        self._tag_role(tk.Label(actions_bar, text="|", bg=t["bg_editor"], fg=t["border"]), "label_ribbon_sep").pack(side="left", padx=1)

        # Box Actions Group (New Box, Cut Box, Copy Box, Paste Box)
        self.ico_plus = self.get_icon("plus", (16, 16))
        self.btn_box_new = self._tag_role(
            tk.Button(actions_bar, text="➕", image=self.ico_plus, fg=btn_fg, bg=btn_bg, activebackground=btn_hover, activeforeground=btn_fg, bd=1, relief="raised", cursor="hand2", command=self.on_box_new),
            "ribbon_btn"
        )
        self.btn_box_new.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_box_new, "New Dialogue Box (Ctrl+N)")

        self.ico_box_cut = self.get_icon("box_cut", (18, 18))
        self.btn_box_cut = self._tag_role(
            tk.Button(actions_bar, text="✂📦", image=self.ico_box_cut, fg=btn_fg, bg=btn_bg, activebackground=btn_hover, activeforeground=btn_fg, bd=1, relief="raised", cursor="hand2", command=self.on_box_cut),
            "ribbon_btn"
        )
        self.btn_box_cut.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_box_cut, "Cut Selected Box(es) (Ctrl+Alt+X)")

        self.ico_box_copy = self.get_icon("box_copy", (18, 18))
        self.btn_box_copy = self._tag_role(
            tk.Button(actions_bar, text="📋📦", image=self.ico_box_copy, fg=btn_fg, bg=btn_bg, activebackground=btn_hover, activeforeground=btn_fg, bd=1, relief="raised", cursor="hand2", command=self.on_box_copy),
            "ribbon_btn"
        )
        self.btn_box_copy.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_box_copy, "Copy Selected Box(es) (Ctrl+Alt+C)")

        self.ico_box_paste = self.get_icon("box_paste", (18, 18))
        self.btn_box_paste = self._tag_role(
            tk.Button(actions_bar, text="📥📦", image=self.ico_box_paste, fg=btn_fg, bg=btn_bg, activebackground=btn_hover, activeforeground=btn_fg, bd=1, relief="raised", cursor="hand2", command=self.on_box_paste),
            "ribbon_btn"
        )
        self.btn_box_paste.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_box_paste, "Paste Box(es) (Ctrl+Alt+V)")

        self._tag_role(tk.Label(ribbon, text="|", bg=t["bg_editor"], fg=t["border"]), "label_ribbon_sep").pack(side="left", padx=1)

        # NGUI Formatting Buttons
        btn_ruby = self._tag_role(
            tk.Button(
                ribbon,
                text="Ruby",
                font=("Segoe UI", 8, "bold"),
                bg=accent_bg,
                fg=fg_accent,
                activebackground=accent_hover,
                activeforeground=fg_accent,
                bd=1,
                relief="raised",
                padx=3,
                pady=0,
                cursor="hand2",
                command=self.on_insert_ruby,
            ),
            "ribbon_primary_btn",
        )
        btn_ruby.pack(side="left", padx=1, pady=1)

        btn_dash = self._tag_role(
            tk.Button(
                ribbon,
                text="[-]",
                font=("Segoe UI", 8, "bold"),
                bg=btn_bg,
                fg=btn_fg,
                activebackground=btn_hover,
                activeforeground=btn_fg,
                bd=1,
                relief="raised",
                padx=2,
                pady=0,
                cursor="hand2",
                command=lambda: self.apply_ngui_wrapper("[-]", ""),
            ),
            "ribbon_btn",
        )
        btn_dash.pack(side="left", padx=1, pady=1)

        self.ico_player = self.get_icon("player", (14, 14))
        btn_player = self._tag_role(
            tk.Button(
                ribbon,
                text=" {0}",
                image=self.ico_player,
                compound="left",
                font=("Segoe UI", 8, "bold"),
                bg=btn_bg,
                fg=btn_fg,
                activebackground=btn_hover,
                activeforeground=btn_fg,
                bd=1,
                relief="raised",
                padx=2,
                pady=0,
                cursor="hand2",
                command=self.on_insert_playername,
            ),
            "ribbon_btn",
        )
        btn_player.pack(side="left", padx=1, pady=1)

        mini_style_buttons = [
            ("B", "[b]", "[/b]"),
            ("I", "[i]", "[/i]"),
            ("U", "[u]", "[/u]"),
            ("S", "[s]", "[/s]"),
            ("Sub", "[sub]", "[/sub]"),
            ("Sup", "[sup]", "[/sup]"),
        ]
        for lbl, o_tag, c_tag in mini_style_buttons:
            w_val = 2 if len(lbl) <= 2 else 3
            f_sz = 8 if len(lbl) <= 2 else 7
            b_mini = self._tag_role(
                tk.Button(
                    ribbon,
                    text=lbl,
                    font=("Segoe UI", f_sz, "bold"),
                    bg=btn_bg,
                    fg=btn_fg,
                    activebackground=btn_hover,
                    activeforeground=btn_fg,
                    bd=1,
                    relief="raised",
                    width=w_val,
                    padx=0,
                    pady=0,
                    cursor="hand2",
                    command=lambda ot=o_tag, ct=c_tag: self.apply_ngui_wrapper(ot, ct),
                ),
                "ribbon_btn",
            )
            b_mini.pack(side="left", padx=1, pady=1)

        btn_size = self._tag_role(
            tk.Button(
                ribbon,
                text="Size",
                font=("Segoe UI", 8, "bold"),
                bg=btn_bg,
                fg=btn_fg,
                activebackground=btn_hover,
                activeforeground=btn_fg,
                bd=1,
                relief="raised",
                padx=2,
                pady=0,
                cursor="hand2",
                command=self._on_size_dropdown_clicked,
            ),
            "ribbon_btn"
        )
        btn_size.pack(side="left", padx=1, pady=1)
        create_tooltip(btn_size, "Change Font Size (<size=...>)")

        self._tag_role(tk.Label(ribbon, text="|", bg=t["bg_editor"], fg=t["border"]), "label_ribbon_sep").pack(side="left", padx=1)

        # History: Undo & Redo with illustrated icons
        self.ico_undo = self.get_icon("undo", (16, 16))
        self.btn_ribbon_undo = self._tag_role(
            tk.Button(
                ribbon,
                text="↶",
                image=self.ico_undo,
                fg=btn_fg,
                bg=btn_bg,
                activebackground=btn_hover,
                activeforeground=btn_fg,
                bd=1,
                relief="raised",
                cursor="hand2",
                command=self.on_undo,
            ),
            "ribbon_undo_btn",
        )
        self.btn_ribbon_undo.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_ribbon_undo, "Undo (Ctrl+Z)")

        self.ico_redo = self.get_icon("redo", (16, 16))
        self.btn_ribbon_redo = self._tag_role(
            tk.Button(
                ribbon,
                text="↷",
                image=self.ico_redo,
                fg=btn_fg,
                bg=btn_bg,
                activebackground=btn_hover,
                activeforeground=btn_fg,
                bd=1,
                relief="raised",
                cursor="hand2",
                command=self.on_redo,
            ),
            "ribbon_redo_btn",
        )
        self.btn_ribbon_redo.pack(side="left", padx=1, pady=1)
        create_tooltip(self.btn_ribbon_redo, "Redo (Ctrl+Y)")

        self.ico_preview = self.get_icon("preview", (16, 16))
        cb_compiled = self._tag_role(
            tk.Checkbutton(
                actions_bar,
                text=" Preview",
                image=self.ico_preview,
                compound="left",
                variable=self.var_preview_compiled,
                command=self._on_toggle_preview_compiled,
                font=("Segoe UI", max(8, u_sz - 2), "bold"),
                bg=t["bg_editor"],
                fg=t["fg_text"],
                selectcolor=t["bg_panel"],
                activebackground=t["bg_editor"],
                activeforeground=t["misora_pink"],
                cursor="hand2",
            ),
            "check_ribbon"
        )
        cb_compiled.pack(side="left", padx=(2, 3), pady=1)

        gutter_bg = "#e8e8e8" if self._is_light_theme() else "#2d2d30"
        gutter_fg = "#707070" if self._is_light_theme() else "#858585"

        # VIEW 1: Bounded Scrollable Page-by-Page Viewport
        self.gd_scroll_wrap = self._tag_role(tk.Frame(top_view, bg=t["bg_panel"]), "panel")
        self.gd_scroll_wrap.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        gd_vscroll = tk.Scrollbar(self.gd_scroll_wrap, orient="vertical")
        gd_vscroll.pack(side="right", fill="y")

        self.gd_canvas = self._tag_role(
            tk.Canvas(
                self.gd_scroll_wrap,
                bg=t["bg_panel"],
                highlightthickness=0,
                bd=0,
                yscrollcommand=gd_vscroll.set,
            ),
            "panel"
        )
        self.gd_canvas.pack(side="left", fill="both", expand=True)
        gd_vscroll.config(command=self._on_gd_scrollbar)

        self.gd_inner = self._tag_role(tk.Frame(self.gd_canvas, bg=t["bg_panel"]), "panel")
        self._gd_canvas_win = self.gd_canvas.create_window((0, 0), window=self.gd_inner, anchor="nw")

        self.gd_inner.bind("<Configure>", self._sync_gd_scroll_bounds)
        self.gd_canvas.bind("<Configure>", self._sync_gd_scroll_bounds)
        self.gd_canvas.bind("<MouseWheel>", self._on_gd_mousewheel)
        self.gd_inner.bind("<MouseWheel>", self._on_gd_mousewheel)

        text_container = self._tag_role(tk.Frame(self.gd_inner, bg=t["bg_panel"]), "panel")
        text_container.pack(fill="both", expand=True, padx=6, pady=(2, 10))

        # Horizontal Column Ruler for Clean View (#12)
        self.ruler_clean = tk.Text(
            text_container,
            height=1,
            font=("Consolas", max(8, d_sz - 2)),
            bg=gutter_bg,
            fg=gutter_fg,
            bd=0,
            relief="flat",
            wrap="none",
            takefocus=0,
            cursor="arrow",
        )
        self.ruler_clean.insert("1.0", "     ....5...10...15...20...25...30...35...40...45...50...55...60...65...70...75...80")
        self.ruler_clean.config(state="disabled")
        if self.show_column_ruler:
            self.ruler_clean.pack(side="top", fill="x", pady=(0, 2))

        self.clean_editor_row = tk.Frame(text_container, bg=t["bg_panel"])
        self.clean_editor_row.pack(fill="both", expand=True)

        # Vertical Line Numbers Gutter for Clean View (#12)
        self.gutter_clean = tk.Text(
            self.clean_editor_row,
            width=3,
            font=("Consolas", d_sz),
            bg=gutter_bg,
            fg=gutter_fg,
            bd=0,
            relief="flat",
            wrap="none",
            takefocus=0,
            cursor="arrow",
            padx=2,
            pady=8,
            spacing1=3,
            spacing3=3,
        )
        self.gutter_clean.config(state="disabled")
        if self.show_line_numbers:
            self.gutter_clean.pack(side="left", fill="y", padx=(0, 2))

        self.txt_dialogue = tk.Text(
            self.clean_editor_row,
            wrap="word",
            height=7,
            font=(d_fam, d_sz),
            bg=t["bg_editor"],
            fg=t["fg_text"],
            insertbackground=t["misora_pink"],
            selectbackground=t["highlight_bg"],
            selectforeground=t["misora_pink"],
            padx=10,
            pady=8,
            spacing1=3,
            spacing3=3,
            bd=1,
            relief="solid",
            highlightthickness=0,
            undo=False,
        )
        self.txt_dialogue.pack(side="left", fill="both", expand=True)
        self._configure_editor_rich_tags(self.txt_dialogue, d_fam, d_sz)
        self.txt_dialogue.bind("<KeyRelease>", lambda e: self._commit_widget_edit(self.txt_dialogue))
        self.txt_dialogue.bind("<<Cut>>", lambda e: self.after_idle(lambda: self._commit_widget_edit(self.txt_dialogue)))
        self.txt_dialogue.bind("<<Paste>>", lambda e: self.after_idle(lambda: self._commit_widget_edit(self.txt_dialogue)))
        self.txt_dialogue.bind("<MouseWheel>", self._on_gd_mousewheel)
        self.txt_dialogue.bind("<Up>", self._on_dialogue_key_up)
        self.txt_dialogue.bind("<Down>", self._on_dialogue_key_down)
        self.txt_dialogue.bind("<Control-z>", lambda e: self._shortcut_undo())
        self.txt_dialogue.bind("<Control-y>", lambda e: self._shortcut_redo())
        self.txt_dialogue.bind("<Control-Shift-Z>", lambda e: self._shortcut_redo())
        self.txt_dialogue.bind("<Control-Shift-z>", lambda e: self._shortcut_redo())
        self.txt_dialogue.bind("<Control-b>", lambda e: self._shortcut_wrap("[b]", "[/b]"))
        self.txt_dialogue.bind("<Control-i>", lambda e: self._shortcut_wrap("[i]", "[/i]"))
        self.txt_dialogue.bind("<Control-u>", lambda e: self._shortcut_wrap("[u]", "[/u]"))
        self.txt_dialogue.bind("<Control-Shift-V>", lambda e: (self.on_paste_cross_box(), "break")[1])
        self.txt_dialogue.bind("<Control-Shift-v>", lambda e: (self.on_paste_cross_box(), "break")[1])

        # Dedicated Box 0 Story Metadata Panel (Option 1)
        self.panel_box0_metadata = self._tag_role(tk.Frame(text_container, bg=t["bg_panel"]), "panel")

        box0_hdr = self._tag_role(tk.Frame(self.panel_box0_metadata, bg=t["bg_panel"]), "panel")
        box0_hdr.pack(fill="x", padx=4, pady=(2, 6))
        self._tag_role(
            tk.Label(
                box0_hdr,
                text="Story Metadata & Cutscene Info (Box 0)",
                font=("Segoe UI", u_sz, "bold"),
                bg=t["bg_panel"],
                fg=t["misora_pink"],
            ),
            "label_accent"
        ).pack(side="left")
        self._tag_role(
            tk.Label(
                box0_hdr,
                text="— Episode title, chapter subtitle, and synopsis summary displayed in cutscene menus",
                font=("Segoe UI", max(8, u_sz - 1), "italic"),
                bg=t["bg_panel"],
                fg=t["fg_muted"],
            ),
            "label_muted"
        ).pack(side="left", padx=6)

        row_title = self._tag_role(tk.Frame(self.panel_box0_metadata, bg=t["bg_panel"]), "panel")
        row_title.pack(fill="x", padx=4, pady=3)
        self._tag_role(
            tk.Label(
                row_title,
                text="Episode Title:",
                width=16,
                anchor="w",
                font=("Segoe UI", u_sz, "bold"),
                bg=t["bg_panel"],
                fg=t["fg_text"],
            ),
            "label_panel"
        ).pack(side="left")
        self.entry_box0_title = self._tag_role(
            tk.Entry(
                row_title,
                textvariable=self.var_box0_title,
                font=(d_fam, d_sz),
                bg=t["bg_editor"],
                fg=t["fg_text"],
                insertbackground=t["misora_pink"],
                relief="solid",
                bd=1,
                highlightthickness=0,
            ),
            "entry_editor"
        )
        self.entry_box0_title.pack(side="left", fill="x", expand=True)
        self.entry_box0_title.bind("<KeyRelease>", lambda e: self._on_box0_metadata_edited())

        row_sub = self._tag_role(tk.Frame(self.panel_box0_metadata, bg=t["bg_panel"]), "panel")
        row_sub.pack(fill="x", padx=4, pady=3)
        self._tag_role(
            tk.Label(
                row_sub,
                text="Chapter Subtitle:",
                width=16,
                anchor="w",
                font=("Segoe UI", u_sz, "bold"),
                bg=t["bg_panel"],
                fg=t["fg_text"],
            ),
            "label_panel"
        ).pack(side="left")
        self.entry_box0_subtitle = self._tag_role(
            tk.Entry(
                row_sub,
                textvariable=self.var_box0_subtitle,
                font=(d_fam, d_sz),
                bg=t["bg_editor"],
                fg=t["fg_text"],
                insertbackground=t["misora_pink"],
                relief="solid",
                bd=1,
                highlightthickness=0,
            ),
            "entry_editor"
        )
        self.entry_box0_subtitle.pack(side="left", fill="x", expand=True)
        self.entry_box0_subtitle.bind("<KeyRelease>", lambda e: self._on_box0_metadata_edited())

        row_sum_hdr = self._tag_role(tk.Frame(self.panel_box0_metadata, bg=t["bg_panel"]), "panel")
        row_sum_hdr.pack(fill="x", padx=4, pady=(6, 2))
        self._tag_role(
            tk.Label(
                row_sum_hdr,
                text="Synopsis / Summary:",
                font=("Segoe UI", u_sz, "bold"),
                bg=t["bg_panel"],
                fg=t["fg_text"],
            ),
            "label_panel"
        ).pack(side="left")
        self.lbl_box0_summary_len = self._tag_role(
            tk.Label(
                row_sum_hdr,
                text="Characters: 0",
                font=("Segoe UI", max(8, u_sz - 1)),
                bg=t["bg_panel"],
                fg=t["fg_muted"],
            ),
            "label_muted"
        )
        self.lbl_box0_summary_len.pack(side="right")

        self.txt_box0_summary = tk.Text(
            self.panel_box0_metadata,
            wrap="word",
            height=6,
            font=(d_fam, d_sz),
            bg=t["bg_editor"],
            fg=t["fg_text"],
            insertbackground=t["misora_pink"],
            selectbackground=t["highlight_bg"],
            selectforeground=t["misora_pink"],
            padx=10,
            pady=8,
            spacing1=3,
            spacing3=3,
            bd=1,
            relief="solid",
            highlightthickness=0,
            undo=False,
        )
        self.txt_box0_summary.pack(fill="both", expand=True, padx=4, pady=(0, 4))
        self._configure_editor_rich_tags(self.txt_box0_summary, d_fam, d_sz)
        self.txt_box0_summary.bind("<KeyRelease>", lambda e: self._on_box0_metadata_edited())
        self.txt_box0_summary.bind("<Control-z>", lambda e: self._shortcut_undo())
        self.txt_box0_summary.bind("<Control-y>", lambda e: self._shortcut_redo())
        self.txt_box0_summary.bind("<Control-Shift-Z>", lambda e: self._shortcut_redo())
        self.txt_box0_summary.bind("<Control-Shift-z>", lambda e: self._shortcut_redo())
        self.txt_box0_summary.bind("<Control-b>", lambda e: self._shortcut_wrap("[b]", "[/b]"))
        self.txt_box0_summary.bind("<Control-i>", lambda e: self._shortcut_wrap("[i]", "[/i]"))
        self.txt_box0_summary.bind("<Control-u>", lambda e: self._shortcut_wrap("[u]", "[/u]"))

        # VIEW 2: Continuous Script Dialog Stream
        self.continuous_wrap = self._tag_role(tk.Frame(top_view, bg=t["bg_panel"]), "panel")

        # Horizontal Column Ruler for Continuous View (#12)
        self.ruler_cont = tk.Text(
            self.continuous_wrap,
            height=1,
            font=("Consolas", max(8, d_sz - 2)),
            bg=gutter_bg,
            fg=gutter_fg,
            bd=0,
            relief="flat",
            wrap="none",
            takefocus=0,
            cursor="arrow",
        )
        self.ruler_cont.insert("1.0", "      ....5...10...15...20...25...30...35...40...45...50...55...60...65...70...75...80")
        self.ruler_cont.config(state="disabled")
        if self.show_column_ruler:
            self.ruler_cont.pack(side="top", fill="x", padx=8, pady=(2, 2))

        self.cont_editor_row = tk.Frame(self.continuous_wrap, bg=t["bg_panel"])
        self.cont_editor_row.pack(fill="both", expand=True, padx=8, pady=(0, 6))

        # Card Stream Canvas & Scrollbar for Multi-Box Story Documents
        self.cont_canvas = tk.Canvas(self.cont_editor_row, bg=t["bg_panel"], highlightthickness=0, bd=0)
        self.cont_scroll_y = tk.Scrollbar(self.cont_editor_row, orient="vertical", command=self.cont_canvas.yview)
        self.cont_canvas.configure(yscrollcommand=self.cont_scroll_y.set)
        self.cont_stream_frame = tk.Frame(self.cont_canvas, bg=t["bg_panel"])
        self.cont_canvas_window = self.cont_canvas.create_window((0, 0), window=self.cont_stream_frame, anchor="nw")

        def _on_cont_canvas_configure(event):
            if hasattr(self, "cont_canvas") and hasattr(self, "cont_canvas_window"):
                new_w = event.width
                if getattr(self, "_cont_resize_job", None) is not None:
                    try:
                        self.after_cancel(self._cont_resize_job)
                    except Exception:
                        pass
                self._cont_resize_job = self.after(20, lambda w=new_w: self._resize_cont_canvas(w))
        self.cont_canvas.bind("<Configure>", _on_cont_canvas_configure)

        def _on_cont_frame_configure(event):
            if hasattr(self, "cont_canvas"):
                self.cont_canvas.configure(scrollregion=self.cont_canvas.bbox("all"))
        self.cont_stream_frame.bind("<Configure>", _on_cont_frame_configure)

        self.cont_canvas.bind("<MouseWheel>", self._on_cont_mousewheel)
        self.cont_stream_frame.bind("<MouseWheel>", self._on_cont_mousewheel)

        # Vertical Line Numbers Gutter for Continuous View (Plain text fallback)
        self.gutter_cont = tk.Text(
            self.cont_editor_row,
            width=4,
            font=("Consolas", max(8, d_sz - 1)),
            bg=gutter_bg,
            fg=gutter_fg,
            bd=0,
            relief="flat",
            wrap="none",
            takefocus=0,
            cursor="arrow",
            padx=2,
            pady=10,
            spacing1=3,
            spacing3=4,
        )
        self.gutter_cont.config(state="disabled")

        self.txt_continuous = tk.Text(
            self.cont_editor_row,
            wrap="word",
            undo=False,
            font=(d_fam, d_sz),
            bg=t["bg_editor"],
            fg=t["fg_text"],
            insertbackground=t["misora_pink"],
            selectbackground=t["highlight_bg"],
            selectforeground=t["misora_pink"],
            padx=14,
            pady=10,
            spacing1=3,
            spacing3=4,
            bd=1,
            relief="solid",
            yscrollcommand=lambda *args: (self.cont_scroll_y.set(*args), self._sync_continuous_gutter_scroll(*args)),
        )

        self.txt_continuous.tag_configure(
            "cont_divider",
            foreground=t["border"],
            font=("Consolas", max(7, d_sz - 3)),
            spacing1=4,
            spacing3=2,
        )
        self.txt_continuous.tag_configure(
            "cont_badge",
            foreground=t["misora_pink"],
            font=("Consolas", max(8, d_sz - 2), "bold"),
            spacing1=2,
            spacing3=4,
        )
        self.txt_continuous.tag_configure(
            "cont_speaker",
            foreground=t["fg_text"],
            font=(d_fam, max(9, d_sz - 1), "bold"),
            spacing1=2,
            spacing3=4,
        )
        self.txt_continuous.tag_configure(
            "cont_narrator",
            foreground=t["fg_muted"],
            font=(d_fam, max(8, d_sz - 2), "italic"),
            spacing1=2,
            spacing3=4,
        )
        self.txt_continuous.tag_configure(
            "cont_voice",
            foreground=t["accent_blue"],
            font=("Segoe UI", max(8, d_sz - 3)),
            spacing1=2,
            spacing3=4,
        )
        self.txt_continuous.tag_configure(
            "cont_active_header",
            background=t["highlight_bg"],
        )
        self.txt_continuous.tag_configure(
            "cont_body",
            foreground=t["fg_text"],
            font=(d_fam, d_sz),
            lmargin1=14,
            lmargin2=14,
            rmargin=10,
        )
        self._configure_editor_rich_tags(self.txt_continuous, d_fam, d_sz)

        self.txt_continuous.bind("<ButtonRelease-1>", self._on_continuous_cursor_moved)
        self.txt_continuous.bind("<Key>", self._on_continuous_key_guard)
        self.txt_continuous.bind("<KeyRelease>", self._on_continuous_key_release)
        self.txt_continuous.bind("<<Copy>>", self._on_continuous_copy)
        self.txt_continuous.bind("<Control-c>", self._on_continuous_copy)
        self.txt_continuous.bind("<<Paste>>", self._on_continuous_paste_guard)
        self.txt_continuous.bind("<<Cut>>", self._on_continuous_cut_guard)
        self.txt_continuous.bind("<Control-b>", lambda e: self._shortcut_wrap("[b]", "[/b]"))
        self.txt_continuous.bind("<Control-i>", lambda e: self._shortcut_wrap("[i]", "[/i]"))
        self.txt_continuous.bind("<Control-u>", lambda e: self._shortcut_wrap("[u]", "[/u]"))
        self.txt_continuous.bind("<Control-Shift-V>", lambda e: (self.on_paste_cross_box(), "break")[1])
        self.txt_continuous.bind("<Control-Shift-v>", lambda e: (self.on_paste_cross_box(), "break")[1])

        # BOTTOM VIEW: Raw AST Script View (Technical Records)
        bottom_view = self._tag_role(tk.Frame(self.v_paned, bg=t["bg_panel"]), "panel")
        self.v_paned.add(bottom_view, minsize=80, height=200, stretch="never")

        raw_header = self._tag_role(tk.Frame(bottom_view, bg=t["bg_panel"]), "panel")
        raw_header.pack(fill="x", padx=8, pady=4)
        self._tag_role(
            tk.Label(raw_header, text="RAW SCRIPT VIEW (Technical AST Records)", font=("Segoe UI", u_sz, "bold"), bg=t["bg_panel"], fg=t["fg_muted"]),
            "label_muted"
        ).pack(side="left")

        raw_container = self._tag_role(tk.Frame(bottom_view, bg=t["bg_panel"]), "panel")
        raw_container.pack(fill="both", expand=True, padx=8, pady=(0, 6))

        raw_scroll_y = tk.Scrollbar(raw_container)
        raw_scroll_y.pack(side="right", fill="y")
        raw_scroll_x = tk.Scrollbar(raw_container, orient="horizontal")
        raw_scroll_x.pack(side="bottom", fill="x")

        self.txt_raw = tk.Text(
            raw_container,
            wrap="none",
            state="disabled",
            font=("Consolas", r_sz),
            bg=self._shift_hex(t["bg_editor"], -6),
            fg=t["fg_muted"],
            insertbackground=t["misora_pink"],
            padx=8,
            pady=6,
            bd=1,
            relief="solid",
            yscrollcommand=raw_scroll_y.set,
            xscrollcommand=raw_scroll_x.set
        )
        self.txt_raw.pack(fill="both", expand=True)
        raw_scroll_y.config(command=self.txt_raw.yview)
        raw_scroll_x.config(command=self.txt_raw.xview)

    # -------------------------------------------------------------------------
    # Debug File Logging & Diagnostics (#14)
    # -------------------------------------------------------------------------
    def _on_debug_settings_changed(self) -> None:
        cats = {cat: (True if cat == ALWAYS_ON_CATEGORY else bool(var.get())) for cat, var in self.var_log_categories.items()}
        self.logger.configure(
            level_name=self.var_log_level.get(),
            log_to_file=bool(self.var_log_to_file.get()),
            categories=cats,
        )
        self._save_user_prefs(silent=True)
        self.logger.info(
            "UI / Theme / Config",
            f"Debug settings updated (level={self.var_log_level.get()}, log_to_file={self.var_log_to_file.get()})",
        )

    def _sync_debug_menu_states(self) -> None:
        exists_state = "normal" if DEBUG_LOG_PATH.is_file() else "disabled"
        try:
            self.debug_menu.entryconfig(self._idx_open_log, state=exists_state)
            self.debug_menu.entryconfig(self._idx_clear_log, state=exists_state)
        except Exception:
            pass

    def _on_open_debug_log_file(self) -> None:
        if not DEBUG_LOG_PATH.is_file():
            messagebox.showinfo("Debug Log", "Debug log file does not exist yet.")
            return
        try:
            if sys.platform == "win32":
                os.startfile(str(DEBUG_LOG_PATH))  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["xdg-open", str(DEBUG_LOG_PATH)])
        except Exception as exc:
            self.logger.error("Errors & Exceptions", f"Failed to open log file: {exc}")

    def _on_clear_debug_log_file(self) -> None:
        if self.logger.clear_log_file():
            self.logger.info("UI / Theme / Config", f"Cleared debug log file: {DEBUG_LOG_PATH}")
            self.show_toast("✓ Cleared debug log file")

    # -------------------------------------------------------------------------
    # Speaker Attributes & Actor Quick Assignment
    # -------------------------------------------------------------------------
    def _on_speaker_dropdown_clicked(self) -> None:
        """Display a clean popup menu of story actors and tools (#18)."""
        if getattr(self, "is_box0_active", False):
            return

        t = self.theme
        panel_fg = best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff")
        menu = tk.Menu(self, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=best_contrast_fg(t["misora_pink"]))

        # Known Story Actors listed directly at top level
        if self.current_doc:
            actors = [a for a in sorted(self.current_doc.actors()) if a]
            for act in actors:
                menu.add_command(
                    label=act,
                    command=lambda a=act: self._assign_speaker_to_current_box(a),
                )
            if actors:
                menu.add_separator()

        menu.add_command(label="Insert {playername}", command=lambda: self._assign_speaker_to_current_box("{playername}"))
        menu.add_command(label="Clear Speaker (Narration)", command=lambda: self._assign_speaker_to_current_box(""))

        try:
            x = self.btn_speaker_dropdown.winfo_rootx()
            y = self.btn_speaker_dropdown.winfo_rooty() + self.btn_speaker_dropdown.winfo_height()
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    def _assign_speaker_to_current_box(self, new_speaker: str) -> None:
        if getattr(self, "is_box0_active", False):
            return
        self.speaker_var.set(new_speaker)
        self._on_speaker_edited()
        self.show_toast(f"Assigned speaker: {new_speaker or '(Narration)'}")

    def _append_speaker_attribute(self, attr_suffix: str) -> None:
        cur = self.speaker_var.get().strip()
        new_val = f"{cur}{attr_suffix}" if cur else attr_suffix
        self.speaker_var.set(new_val)
        self._on_speaker_edited()
        self.show_toast(f"Updated speaker: {new_val}")

    def _prompt_append_speaker_attribute(self) -> None:
        """Modal prompt to append a custom attribute/variant to current speaker."""
        t = self.theme
        dlg = tk.Toplevel(self)
        dlg.title("Append Speaker Attribute")
        dlg.geometry("380x150")
        dlg.resizable(False, False)
        dlg.transient(self)
        dlg.grab_set()
        dlg.configure(bg=t["bg_panel"])
        apply_window_icon(dlg)

        tk.Label(dlg, text="Enter Attribute (e.g. （サマー） or (Summer)):", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=best_contrast_fg(t["bg_panel"])).pack(padx=14, pady=(14, 6), anchor="w")
        var_attr = tk.StringVar(master=dlg, value="（サマー）")
        ent = tk.Entry(dlg, textvariable=var_attr, font=("Segoe UI", 10), bg=t["bg_editor"], fg=best_contrast_fg(t["bg_editor"]))
        ent.pack(fill="x", padx=14, pady=4)
        ent.focus_set()
        ent.select_range(0, tk.END)

        btn_row = tk.Frame(dlg, bg=t["bg_panel"])
        btn_row.pack(fill="x", padx=14, pady=10)

        def _safe_close(_e: Optional[tk.Event] = None):
            safe_grab_release(dlg)
            dlg.destroy()

        def _commit():
            val = var_attr.get().strip()
            if val:
                self._append_speaker_attribute(val)
            _safe_close()

        dlg.protocol("WM_DELETE_WINDOW", _safe_close)
        dlg.bind("<Escape>", _safe_close)
        ent.bind("<Return>", lambda e: _commit())
        ttk.Button(btn_row, text="Append", style="Pink.TButton", command=_commit).pack(side="right", padx=(4, 0))
        ttk.Button(btn_row, text="Cancel", style="TButton", command=_safe_close).pack(side="right")

    # -------------------------------------------------------------------------
    # Line Numbers Gutter & Column Ruler Synchronization (#12)
    # -------------------------------------------------------------------------
    @staticmethod
    def _is_widget_packed(w: tk.Widget) -> bool:
        try:
            return bool(w.pack_info())
        except Exception:
            return False

    def _on_toggle_line_numbers(self) -> None:
        """Toggle line number gutter visibility with safe layout anchoring."""
        visible = bool(self.var_show_line_numbers.get())
        self.show_line_numbers = visible

        # Clean View gutter
        if hasattr(self, "gutter_clean"):
            if visible:
                if hasattr(self, "txt_dialogue") and not self._is_widget_packed(self.gutter_clean):
                    try:
                        self.gutter_clean.pack(before=self.txt_dialogue, side="left", fill="y", padx=(0, 2))
                    except Exception:
                        self.gutter_clean.pack(side="left", fill="y", padx=(0, 2))
                self._update_gutter_clean()
            else:
                if self._is_widget_packed(self.gutter_clean):
                    self.gutter_clean.pack_forget()

        # Continuous View card gutters
        if hasattr(self, "_card_widgets"):
            for idx, cdata in self._card_widgets.items():
                gutter = cdata.get("gutter")
                txt = cdata.get("txt")
                if gutter and txt:
                    if visible:
                        if not self._is_widget_packed(gutter):
                            try:
                                gutter.pack(before=txt, side="left", fill="y", padx=(0, 2))
                            except Exception:
                                gutter.pack(side="left", fill="y", padx=(0, 2))
                    else:
                        if self._is_widget_packed(gutter):
                            gutter.pack_forget()

        # Plain text fallback gutter
        if hasattr(self, "gutter_cont") and hasattr(self, "txt_continuous"):
            if visible and self._is_widget_packed(self.txt_continuous) and not self._is_widget_packed(self.gutter_cont):
                try:
                    self.gutter_cont.pack(before=self.txt_continuous, side="left", fill="y", padx=(0, 2))
                except Exception:
                    self.gutter_cont.pack(side="left", fill="y", padx=(0, 2))
            elif not visible and self._is_widget_packed(self.gutter_cont):
                self.gutter_cont.pack_forget()

        if hasattr(self, "cont_canvas"):
            self.cont_canvas.configure(scrollregion=self.cont_canvas.bbox("all"))
        if hasattr(self, "gd_inner"):
            self.gd_inner.update_idletasks()
            self._sync_gd_scroll_bounds()
        self.show_toast(f"Line numbers {'enabled' if visible else 'hidden'}")
        self._save_user_prefs(silent=True)

    def _on_toggle_column_ruler(self) -> None:
        """Toggle column ruler visibility with safe layout anchoring."""
        visible = bool(self.var_show_column_ruler.get())
        self.show_column_ruler = visible
        if hasattr(self, "ruler_clean"):
            if visible:
                if hasattr(self, "clean_editor_row") and not self._is_widget_packed(self.ruler_clean):
                    try:
                        self.ruler_clean.pack(before=self.clean_editor_row, side="top", fill="x", pady=(0, 2))
                    except Exception:
                        self.ruler_clean.pack(side="top", fill="x", pady=(0, 2))
            else:
                if self._is_widget_packed(self.ruler_clean):
                    self.ruler_clean.pack_forget()
        if hasattr(self, "ruler_cont"):
            if visible:
                if hasattr(self, "cont_editor_row") and not self._is_widget_packed(self.ruler_cont):
                    try:
                        self.ruler_cont.pack(before=self.cont_editor_row, side="top", fill="x", padx=8, pady=(2, 2))
                    except Exception:
                        self.ruler_cont.pack(side="top", fill="x", padx=8, pady=(2, 2))
            else:
                if self._is_widget_packed(self.ruler_cont):
                    self.ruler_cont.pack_forget()
        if hasattr(self, "gd_inner"):
            self.gd_inner.update_idletasks()
            self._sync_gd_scroll_bounds()
        self.show_toast(f"Column ruler {'enabled' if visible else 'hidden'}")
        self._save_user_prefs(silent=True)

    def _update_gutter_clean(self) -> None:
        """Update line numbers in clean dialogue view gutter."""
        if not hasattr(self, "gutter_clean"):
            return
        try:
            total_lines = int(self.txt_dialogue.index("end-1c").split(".")[0])
            numbers = "\n".join(f"{i:>2} " for i in range(1, max(1, total_lines) + 1))
            self.gutter_clean.config(state="normal")
            self.gutter_clean.delete("1.0", tk.END)
            self.gutter_clean.insert("1.0", numbers)
            self.gutter_clean.config(state="disabled")
        except Exception:
            pass

    def _update_gutter_cont(self, line_num_list: List[str]) -> None:
        """Update repeating per-box line numbers in continuous view gutter."""
        if not hasattr(self, "gutter_cont"):
            return
        try:
            self.gutter_cont.config(state="normal")
            self.gutter_cont.delete("1.0", tk.END)
            self.gutter_cont.insert("1.0", "\n".join(line_num_list))
            self.gutter_cont.config(state="disabled")
        except Exception:
            pass

    def _sync_continuous_gutter_scroll(self, *args) -> None:
        """Keep line number gutter perfectly scrolled in lockstep with continuous text."""
        if hasattr(self, "gutter_cont") and self.show_line_numbers:
            try:
                self.gutter_cont.yview_moveto(args[0])
            except Exception:
                pass

    def _on_continuous_vscroll(self, *args) -> None:
        """Handle vertical scrollbar motion for both text and gutter."""
        try:
            self.txt_continuous.yview(*args)
            if hasattr(self, "gutter_cont") and self.show_line_numbers:
                self.gutter_cont.yview(*args)
        except Exception:
            pass

    def _highlight_secret_whitespace(self, text_widget: tk.Text) -> None:
        """Clear any residual whitespace highlighting to prevent visual artifacts."""
        try:
            text_widget.tag_remove("secret_whitespace", "1.0", tk.END)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # NGUI Attributes Ribbon Actions & Compiled Preview Compiler
    # -------------------------------------------------------------------------
    def _shortcut_wrap(self, open_tag: str, close_tag: str) -> str:
        self.apply_ngui_wrapper(open_tag, close_tag)
        return "break"

    def _shortcut_undo(self) -> str:
        self.on_undo()
        return "break"

    def _shortcut_redo(self) -> str:
        self.on_redo()
        return "break"

    def _set_ribbon_colors(self, primary_hex: str, secondary_hex: str) -> None:
        if HEX_COLOR_RE.match(primary_hex):
            self._active_ngui_color = primary_hex.lower()
            if hasattr(self, "btn_ribbon_swatch"):
                self.btn_ribbon_swatch.configure(
                    bg=self._active_ngui_color,
                    activebackground=self._active_ngui_color,
                )
        if HEX_COLOR_RE.match(secondary_hex):
            self._active_ngui_grad_end = secondary_hex.lower()

    def _apply_active_ribbon_color(self) -> None:
        code = self._active_ngui_color[1:].upper()
        self.apply_ngui_wrapper(f"[{code}]", "[-]")

    def _apply_active_ribbon_gradient(self) -> None:
        c0 = self._active_ngui_color[1:].upper()
        c1 = self._active_ngui_grad_end[1:].upper()
        self.apply_ngui_wrapper(f"[{c0}-{c1}]", "[-]")

    def on_open_color_picker(self) -> None:
        self.logger.info(
            "UI / Theme / Config",
            f"Opening NGUI Color & Gradient Picker (primary={self._active_ngui_color}, secondary={self._active_ngui_grad_end})",
        )
        if self._color_picker_win is not None and self._color_picker_win.winfo_exists():
            self._color_picker_win.lift()
            self._color_picker_win.focus_set()
            return
        self._color_picker_win = NguiColorPickerPopup(
            self,
            primary_hex=self._active_ngui_color,
            secondary_hex=self._active_ngui_grad_end,
        )

