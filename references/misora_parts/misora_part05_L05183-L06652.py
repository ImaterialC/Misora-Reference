# ======================================================================
# FILE: misora.py — PART 05 / 10
# ORIGINAL LINE RANGE : L5183 .. L6652 (total 1470 lines of 12835)
# SOURCE SHA-256      : d23baae2be82fe93a18da7d3769af30d19ebe02a8b5f6a3645d56a6f53c0710e
# NOTE FOR AI REVIEWER: Cite ORIGINAL line numbers (L5183..L6652) and symbol names.
# SYMBOLS IN THIS PART (with exact original line numbers):
#   L05183:   MisoraApp.apply_ngui_wrapper (def)
#   L05193:   MisoraApp._on_toggle_preview_compiled (def)
#   L05205:   MisoraApp._get_or_create_compiled_style_tag (def)
#   L05241:   MisoraApp._insert_compiled_ngui_text (def)
#   L05379:   MisoraApp._build_side_drawer (def)
#   L05431:   MisoraApp._build_customize_tab (def)
#   L05588:   MisoraApp._build_glossary_tab (def)
#   L05660:   MisoraApp._open_side_drawer (def)
#   L05666:   MisoraApp._close_side_drawer (def)
#   L05671:   MisoraApp._toggle_side_drawer (def)
#   L05677:   MisoraApp._switch_side_drawer_tab (def)
#   L05690:   MisoraApp._on_font_pref_changed (def)
#   L05717:   MisoraApp._adjust_dialogue_font_size (def)
#   L05725:   MisoraApp._pick_theme_color (def)
#   L05742:   MisoraApp._commit_theme_hex (def)
#   L05764:   MisoraApp._apply_theme_preset (def)
#   L05787:   MisoraApp._reset_customization_defaults (def)
#   L05809:   MisoraApp._filter_glossary (def)
#   L05824:   MisoraApp._render_glossary_list (def)
#   L05848:   MisoraApp._on_glossary_click (def)
#   L05857:   MisoraApp._on_glossary_double_click (def)
#   L05862:   MisoraApp._insert_selected_glossary_tag (def)
#   L05877:   MisoraApp._insert_text_wrapper (def)
#   L05930:   MisoraApp.on_insert_ruby (def)
#   L06057:   MisoraApp._highlight_ngui_tags (def)
#   L06089:   MisoraApp._sync_gd_scroll_bounds (def)
#   L06102:   MisoraApp._on_gd_scrollbar (def)
#   L06109:   MisoraApp._on_gd_mousewheel (def)
#   L06131:   MisoraApp._auto_resize_dialogue_box (def)
#   L06141:   MisoraApp._on_toggle_continuous_view (def)
#   L06196:   MisoraApp._build_status_bar (def)
#   L06227:   MisoraApp._toggle_console_shortcut (def)
#   L06231:   MisoraApp._get_active_text_widget (def)
#   L06253:   MisoraApp._get_card_text_widget (def)
#   L06269:   MisoraApp._install_shortcuts_bindtag (def)
#   L06278:   MisoraApp._on_misora_shortcut (def)
#   L06385:   MisoraApp._show_csif_paste_chooser (def)
#   L06526:   MisoraApp._handle_editor_csif_paste (def)
#   L06544:   MisoraApp._bind_shortcuts (def)
#   L06596:   MisoraApp._toggle_continuous_shortcut (def)
#   L06603:   MisoraApp._flush_active_widget (def)
# ======================================================================

    def apply_ngui_wrapper(self, open_tag: str, close_tag: str, default_inner: str = "") -> None:
        """Ensure Raw Edit mode is active, then wrap selection or insert NGUI tags at caret."""
        if self.var_preview_compiled.get():
            self.var_preview_compiled.set(False)
            self._update_views()
        self._insert_text_wrapper(open_tag, close_tag, default_inner=default_inner)
        target = self._get_active_text_widget()
        if target:
            self._commit_widget_edit(target)

    def _on_toggle_preview_compiled(self) -> None:
        """Toggle between editable raw NGUI tags and compiled visual preview."""
        if self.var_preview_compiled.get():
            self.lbl_status.config(
                text="Compiled Attribute Preview ON (read-only) — uncheck 'Compiled' to edit raw tags."
            )
        else:
            self.lbl_status.config(
                text="Raw NGUI Tag Edit Mode active."
            )
        self._update_views()

    def _get_or_create_compiled_style_tag(
        self,
        widget: tk.Text,
        bold: bool,
        italic: bool,
        underline: bool,
        strike: bool,
        sub_mode: int,
        fg_color: Optional[str],
        font_scale: float = 1.0,
    ) -> str:
        """Return a cached Tkinter tag name configured with the requested compiled NGUI style."""
        d_fam = self.prefs.get("dialogue_font_family", "Segoe UI")
        d_sz = int(self.prefs.get("dialogue_font_size", 12))
        eff_sz = max(7, d_sz - 2) if sub_mode != 0 else d_sz
        if font_scale != 1.0:
            eff_sz = max(7, int(round(eff_sz * font_scale)))
        eff_offset = -3 if sub_mode < 0 else (4 if sub_mode > 0 else 0)
        color_key = fg_color.lower() if fg_color else "default"
        tag_name = f"cstyle_{int(bold)}_{int(italic)}_{int(underline)}_{int(strike)}_{sub_mode}_{color_key}_{d_fam}_{eff_sz}"

        if tag_name not in widget.tag_names():
            weight = "bold" if bold else "normal"
            slant = "italic" if italic else "roman"
            font_tuple = (d_fam, eff_sz, weight, slant)
            cfg: Dict[str, Any] = {
                "font": font_tuple,
                "underline": underline,
                "overstrike": strike,
                "offset": eff_offset,
            }
            if fg_color:
                cfg["foreground"] = fg_color
            widget.tag_configure(tag_name, **cfg)
        return tag_name

    def _insert_compiled_ngui_text(
        self,
        widget: tk.Text,
        insert_pos: str,
        raw_text: str,
        base_tags: Tuple[str, ...] = (),
    ) -> None:
        """Parse NGUI/Priconne markup in `raw_text` and insert compiled rich text into `widget`."""
        mark_name = f"_compile_ins_{id(widget)}"
        widget.mark_set(mark_name, insert_pos)
        widget.mark_gravity(mark_name, tk.RIGHT)

        bold = False
        italic = False
        underline = False
        strike = False
        sub_mode = 0
        font_scale = 1.0
        color_stack: List[Tuple[str, Optional[str]]] = []

        def emit_styled_run(chunk: str) -> None:
            if not chunk:
                return
            chunk = chunk.replace("\\n", "\n")
            if not color_stack:
                st = self._get_or_create_compiled_style_tag(
                    widget, bold, italic, underline, strike, sub_mode, None, font_scale
                )
                widget.insert(mark_name, chunk, base_tags + (st,))
                return

            top_hex, bot_hex = color_stack[-1]
            if not bot_hex or len(chunk) <= 1:
                st = self._get_or_create_compiled_style_tag(
                    widget, bold, italic, underline, strike, sub_mode, top_hex, font_scale
                )
                widget.insert(mark_name, chunk, base_tags + (st,))
                return

            r1, g1, b1 = int(top_hex[1:3], 16), int(top_hex[3:5], 16), int(top_hex[5:7], 16)
            r2, g2, b2 = int(bot_hex[1:3], 16), int(bot_hex[3:5], 16), int(bot_hex[5:7], 16)
            denom = max(1, len(chunk) - 1)
            for idx, ch in enumerate(chunk):
                ratio = idx / denom
                ri = int(round(r1 + (r2 - r1) * ratio))
                gi = int(round(g1 + (g2 - g1) * ratio))
                bi = int(round(b1 + (b2 - b1) * ratio))
                step_hex = f"#{ri:02x}{gi:02x}{bi:02x}"
                st = self._get_or_create_compiled_style_tag(
                    widget, bold, italic, underline, strike, sub_mode, step_hex, font_scale
                )
                widget.insert(mark_name, ch, base_tags + (st,))

        last_idx = 0
        try:
            for m in NGUI_TOKEN_RE.finditer(raw_text):
                if m.start() > last_idx:
                    emit_styled_run(raw_text[last_idx:m.start()])

                tok = m.group(0)
                tok_low = tok.lower()

                if m.group(2) is not None:
                    ruby_txt = m.group(2).replace("\\n", "\n")
                    base_txt = m.group(3)
                    emit_styled_run(base_txt)
                    if ruby_txt:
                        widget.insert(mark_name, ruby_txt, base_tags + ("compiled_ruby",))
                elif tok_low == "[b]":
                    bold = True
                elif tok_low == "[/b]":
                    bold = False
                elif tok_low == "[i]":
                    italic = True
                elif tok_low == "[/i]":
                    italic = False
                elif tok_low == "[u]":
                    underline = True
                elif tok_low == "[/u]":
                    underline = False
                elif tok_low == "[s]":
                    strike = True
                elif tok_low == "[/s]":
                    strike = False
                elif tok_low == "[sub]":
                    sub_mode = -1
                elif tok_low == "[/sub]":
                    sub_mode = 0
                elif tok_low == "[sup]":
                    sub_mode = 1
                elif tok_low == "[/sup]":
                    sub_mode = 0
                elif tok_low.startswith("<size=") or tok_low.startswith("[size="):
                    try:
                        val = tok[6:-1].strip()
                        if val.endswith("%"):
                            font_scale = max(0.5, min(3.0, float(val[:-1]) / 100.0))
                        else:
                            base_d_sz = int(self.prefs.get("dialogue_font_size", 12))
                            font_scale = max(0.5, min(3.0, float(val) / base_d_sz))
                    except Exception:
                        font_scale = 1.0
                elif tok_low in ("</size>", "[/size]"):
                    font_scale = 1.0
                elif tok_low == "[/]":
                    bold = False
                    italic = False
                    underline = False
                    strike = False
                    sub_mode = 0
                    font_scale = 1.0
                elif tok_low in ("[c]", "[/c]", "[/url]") or tok_low.startswith("[url="):
                    pass
                elif tok == "[-]":
                    if color_stack:
                        color_stack.pop()
                elif m.group(4) is not None:
                    c1 = "#" + m.group(4).lower()[:6]
                    c2 = ("#" + m.group(5).lower()[:6]) if m.group(5) else None
                    color_stack.append((c1, c2))
                elif tok in ("{playername}", "{0}"):
                    widget.insert(mark_name, "{playername}", base_tags + ("compiled_player",))
                else:
                    emit_styled_run(tok)

                last_idx = m.end()

            if last_idx < len(raw_text):
                emit_styled_run(raw_text[last_idx:])
        finally:
            try:
                widget.mark_unset(mark_name)
            except Exception:
                pass

    # -------------------------------------------------------------------------
    # Embedded Side Drawer: Customization & NGUI Glossary Help
    # -------------------------------------------------------------------------
    def _build_side_drawer(self) -> None:
        """Build dockable right-hand side panel for Display Customization & NGUI Glossary."""
        t = self.theme
        self.side_drawer = self._tag_role(tk.Frame(self.h_paned, bg=t["bg_panel"]), "panel")

        drawer_top = self._tag_role(tk.Frame(self.side_drawer, bg=t["bg_panel"]), "panel")
        drawer_top.pack(fill="x", padx=6, pady=(6, 4))

        self.btn_tab_customize = ttk.Button(
            drawer_top,
            text="Customize",
            style="Pink.TButton",
            command=lambda: self._switch_side_drawer_tab("customize"),
        )
        self.btn_tab_customize.pack(side="left", padx=(0, 4))

        self.btn_tab_glossary = ttk.Button(
            drawer_top,
            text="NGUI Glossary",
            style="TButton",
            command=lambda: self._switch_side_drawer_tab("glossary"),
        )
        self.btn_tab_glossary.pack(side="left")

        self.btn_close_drawer = ttk.Button(
            drawer_top,
            text="✕",
            style="Small.TButton",
            command=self._close_side_drawer,
            width=2,
        )
        self.btn_close_drawer.pack(side="right", padx=(2, 0))
        create_tooltip(self.btn_close_drawer, "Close Side Panel")

        self.btn_drawer_pin = ttk.Button(
            drawer_top,
            text="📌",
            style="Small.TButton",
            command=self._toggle_side_drawer_pin,
            width=3,
        )
        self.btn_drawer_pin.pack(side="right", padx=(2, 2))
        create_tooltip(self.btn_drawer_pin, "Pin / Unpin Side Panel")

        self.tab_customize_frame = self._tag_role(tk.Frame(self.side_drawer, bg=t["bg_panel"]), "panel")
        self._build_customize_tab(self.tab_customize_frame)

        self.tab_glossary_frame = self._tag_role(tk.Frame(self.side_drawer, bg=t["bg_panel"]), "panel")
        self._build_glossary_tab(self.tab_glossary_frame)

        self._switch_side_drawer_tab("customize")

    def _build_customize_tab(self, parent: tk.Frame) -> None:
        """Populate font size controls, theme presets, and custom color pickers."""
        t = self.theme
        wrap = self._tag_role(tk.Frame(parent, bg=t["bg_editor"], bd=1, relief="solid"), "editor_box")
        wrap.pack(fill="both", expand=True, padx=4, pady=(0, 6))

        canvas = self._tag_role(tk.Canvas(wrap, bg=t["bg_panel"], highlightthickness=0, bd=0), "panel")
        vscroll = tk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
        vscroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=vscroll.set)

        body = self._tag_role(tk.Frame(canvas, bg=t["bg_panel"]), "panel")
        win_id = canvas.create_window((0, 0), window=body, anchor="nw")

        body.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(win_id, width=max(220, e.width)))

        self._tag_role(
            tk.Label(body, text="FONT & DISPLAY PREFERENCES", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"]),
            "label_accent"
        ).pack(anchor="w", padx=8, pady=(8, 6))

        fam_row = self._tag_role(tk.Frame(body, bg=t["bg_panel"]), "panel")
        fam_row.pack(fill="x", padx=8, pady=3)
        self._tag_role(tk.Label(fam_row, text="Dialogue Font:", bg=t["bg_panel"], fg=t["fg_text"]), "label_panel").pack(side="left")

        self.var_font_family = tk.StringVar(master=self, value=self.prefs["dialogue_font_family"])
        cb_font = ttk.Combobox(
            fam_row,
            textvariable=self.var_font_family,
            values=["Segoe UI", "Meiryo UI", "Yu Gothic UI", "Consolas", "Arial"],
            state="readonly",
            width=15,
        )
        cb_font.pack(side="right")
        cb_font.bind("<<ComboboxSelected>>", lambda _e: self._on_font_pref_changed())

        self.var_dlg_font_sz = tk.IntVar(master=self, value=int(self.prefs["dialogue_font_size"]))
        self.var_raw_font_sz = tk.IntVar(master=self, value=int(self.prefs["raw_font_size"]))
        self.var_ui_font_sz = tk.IntVar(master=self, value=int(self.prefs["ui_font_size"]))

        font_rows = [
            ("Dialogue Size (pt):", self.var_dlg_font_sz, 8, 28),
            ("Raw Script Size (pt):", self.var_raw_font_sz, 7, 22),
            ("UI & Search Size (pt):", self.var_ui_font_sz, 8, 16),
        ]
        for label_txt, int_var, min_v, max_v in font_rows:
            r = self._tag_role(tk.Frame(body, bg=t["bg_panel"]), "panel")
            r.pack(fill="x", padx=8, pady=3)
            self._tag_role(tk.Label(r, text=label_txt, bg=t["bg_panel"], fg=t["fg_text"]), "label_panel").pack(side="left")
            sb = tk.Spinbox(
                r,
                from_=min_v,
                to=max_v,
                textvariable=int_var,
                width=6,
                font=("Consolas", 9),
                bg=t["bg_editor"],
                fg=t["fg_text"],
                buttonbackground=t["bg_panel"],
                relief="solid",
                bd=1,
                command=self._on_font_pref_changed,
            )
            sb.pack(side="right")
            sb.bind("<Return>", lambda _e: self._on_font_pref_changed())
            sb.bind("<FocusOut>", lambda _e: self._on_font_pref_changed())

        self._tag_role(
            tk.Label(body, text="THEME PRESETS", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"]),
            "label_accent"
        ).pack(anchor="w", padx=8, pady=(12, 4))

        preset_row = self._tag_role(tk.Frame(body, bg=t["bg_panel"]), "panel")
        preset_row.pack(fill="x", padx=8, pady=3)
        self.var_preset = tk.StringVar(master=self, value=self._detect_active_preset_name())
        cb_preset = ttk.Combobox(
            preset_row,
            textvariable=self.var_preset,
            values=list(THEME_PRESETS.keys()) + ["Custom"],
            state="readonly",
            width=22,
        )
        cb_preset.pack(side="left", fill="x", expand=True, padx=(0, 4))
        cb_preset.bind("<<ComboboxSelected>>", lambda _e: self._apply_theme_preset(self.var_preset.get()))
        ttk.Button(
            preset_row,
            text="Apply",
            style="Small.TButton",
            command=lambda: self._apply_theme_preset(self.var_preset.get()),
        ).pack(side="right")

        self._tag_role(
            tk.Label(body, text="CUSTOM WINDOW COLORS", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"]),
            "label_accent"
        ).pack(anchor="w", padx=8, pady=(12, 4))

        color_specs = [
            ("bg_dark", "Window Background"),
            ("bg_panel", "Panel Surface"),
            ("bg_editor", "Editor Surface"),
            ("misora_pink", "Primary Accent"),
            ("fg_text", "Primary Text"),
            ("fg_muted", "Secondary Text"),
            ("highlight_bg", "Selection / Hit BG"),
            ("border", "Divider / Border"),
        ]

        for key, label_txt in color_specs:
            row = self._tag_role(tk.Frame(body, bg=t["bg_panel"]), "panel")
            row.pack(fill="x", padx=8, pady=3)

            self._tag_role(tk.Label(row, text=label_txt, bg=t["bg_panel"], fg=t["fg_text"]), "label_panel").pack(side="left")

            swatch = tk.Button(
                row,
                width=3,
                bg=t[key],
                activebackground=t[key],
                relief="solid",
                bd=1,
                cursor="hand2",
                command=lambda k=key: self._pick_theme_color(k),
            )
            swatch.pack(side="right", padx=(4, 0))
            self._theme_swatch_buttons[key] = swatch

            hvar = tk.StringVar(master=self, value=t[key])
            self._theme_hex_vars[key] = hvar
            hex_ent = self._tag_role(
                tk.Entry(
                    row,
                    textvariable=hvar,
                    width=9,
                    font=("Consolas", 9),
                    bg=t["bg_editor"],
                    fg=t["fg_text"],
                    insertbackground=t["misora_pink"],
                    bd=1,
                    relief="solid",
                ),
                "entry_editor"
            )
            hex_ent.pack(side="right")
            hex_ent.bind("<Return>", lambda _e, k=key: self._commit_theme_hex(k))
            hex_ent.bind("<FocusOut>", lambda _e, k=key: self._commit_theme_hex(k))

        btn_row = self._tag_role(tk.Frame(body, bg=t["bg_panel"]), "panel")
        btn_row.pack(fill="x", padx=8, pady=(12, 10))
        ttk.Button(
            btn_row,
            text="Reset All to Defaults",
            style="TButton",
            command=self._reset_customization_defaults,
        ).pack(fill="x")

    def _build_glossary_tab(self, parent: tk.Frame) -> None:
        """Populate interactive NGUI Glossary & Syntax Reference panel."""
        t = self.theme
        u_sz = int(self.prefs["ui_font_size"])

        filter_row = self._tag_role(tk.Frame(parent, bg=t["bg_panel"]), "panel")
        filter_row.pack(fill="x", padx=6, pady=(2, 4))

        self._tag_role(tk.Label(filter_row, text="Filter:", bg=t["bg_panel"], fg=t["fg_muted"]), "label_muted").pack(side="left", padx=(0, 4))
        self.var_glossary_filter = tk.StringVar(master=self)
        ent_filter = self._tag_role(
            tk.Entry(
                filter_row,
                textvariable=self.var_glossary_filter,
                font=("Segoe UI", 9),
                bg=t["bg_editor"],
                fg=t["fg_text"],
                insertbackground=t["misora_pink"],
                bd=1,
                relief="solid",
            ),
            "entry_editor"
        )
        ent_filter.pack(side="left", fill="x", expand=True)
        ent_filter.bind("<KeyRelease>", lambda _e: self._filter_glossary())

        list_wrap = self._tag_role(tk.Frame(parent, bg=t["bg_editor"], bd=1, relief="solid"), "editor_box")
        list_wrap.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        g_scroll = tk.Scrollbar(list_wrap, orient="vertical")
        g_scroll.pack(side="right", fill="y")

        self.txt_glossary = tk.Text(
            list_wrap,
            wrap="word",
            font=("Segoe UI", u_sz),
            bg=t["bg_editor"],
            fg=t["fg_text"],
            insertwidth=0,
            cursor="hand2",
            padx=8,
            pady=6,
            bd=0,
            relief="flat",
            exportselection=False,
            state="disabled",
            yscrollcommand=g_scroll.set,
        )
        self.txt_glossary.pack(side="left", fill="both", expand=True)
        g_scroll.config(command=self.txt_glossary.yview)

        self.txt_glossary.tag_configure("gl_tag", font=("Consolas", u_sz, "bold"), foreground=t["misora_pink"])
        self.txt_glossary.tag_configure("gl_title", font=("Segoe UI", u_sz, "bold"), foreground=t["fg_text"])
        self.txt_glossary.tag_configure("gl_syntax", font=("Consolas", max(8, u_sz - 1)), foreground=t["accent_blue"])
        self.txt_glossary.tag_configure("gl_desc", font=("Segoe UI", max(8, u_sz - 1)), foreground=t["fg_muted"])
        self.txt_glossary.tag_configure("gl_selected", background=t["highlight_bg"])

        self.txt_glossary.bind("<Button-1>", self._on_glossary_click)
        self.txt_glossary.bind("<Double-Button-1>", self._on_glossary_double_click)

        ins_bar = self._tag_role(tk.Frame(parent, bg=t["bg_panel"]), "panel")
        ins_bar.pack(fill="x", padx=6, pady=(0, 6))

        ttk.Button(
            ins_bar,
            text="Insert / Wrap Selected Tag into Dialogue",
            style="Pink.TButton",
            command=self._insert_selected_glossary_tag,
        ).pack(fill="x")

        self._render_glossary_list()

    def _open_side_drawer(self, tab: str = "customize") -> None:
        if not self._side_drawer_visible:
            self.h_paned.add(self.side_drawer, minsize=260, width=330, stretch="never")
            self._side_drawer_visible = True
        self._switch_side_drawer_tab(tab)

    def _close_side_drawer(self) -> None:
        if self._side_drawer_visible:
            self.h_paned.forget(self.side_drawer)
            self._side_drawer_visible = False

    def _toggle_side_drawer(self, tab: str) -> None:
        if self._side_drawer_visible and self._side_drawer_tab == tab:
            self._close_side_drawer()
        else:
            self._open_side_drawer(tab)

    def _switch_side_drawer_tab(self, tab: str) -> None:
        self._side_drawer_tab = tab
        if tab == "customize":
            self.tab_glossary_frame.pack_forget()
            self.tab_customize_frame.pack(fill="both", expand=True)
            self.btn_tab_customize.configure(style="Pink.TButton")
            self.btn_tab_glossary.configure(style="TButton")
        else:
            self.tab_customize_frame.pack_forget()
            self.tab_glossary_frame.pack(fill="both", expand=True)
            self.btn_tab_customize.configure(style="TButton")
            self.btn_tab_glossary.configure(style="Pink.TButton")

    def _on_font_pref_changed(self) -> None:
        """Apply updated font family / size values from Customize panel."""
        fam = self.var_font_family.get().strip() or self.prefs["dialogue_font_family"]
        try:
            d_sz = max(8, min(28, int(self.var_dlg_font_sz.get())))
        except Exception:
            d_sz = int(self.prefs["dialogue_font_size"])
            self.var_dlg_font_sz.set(d_sz)

        try:
            r_sz = max(7, min(22, int(self.var_raw_font_sz.get())))
        except Exception:
            r_sz = int(self.prefs["raw_font_size"])
            self.var_raw_font_sz.set(r_sz)

        try:
            u_sz = max(8, min(16, int(self.var_ui_font_sz.get())))
        except Exception:
            u_sz = int(self.prefs["ui_font_size"])
            self.var_ui_font_sz.set(u_sz)

        self.prefs["dialogue_font_family"] = fam
        self.prefs["dialogue_font_size"] = d_sz
        self.prefs["raw_font_size"] = r_sz
        self.prefs["ui_font_size"] = u_sz
        self._apply_theme_and_fonts_live(save=True)

    def _adjust_dialogue_font_size(self, delta: int) -> None:
        cur = int(self.prefs["dialogue_font_size"])
        new_sz = max(8, min(28, cur + delta))
        self.prefs["dialogue_font_size"] = new_sz
        if hasattr(self, "var_dlg_font_sz"):
            self.var_dlg_font_sz.set(new_sz)
        self._apply_theme_and_fonts_live(save=True)

    def _pick_theme_color(self, key: str) -> None:
        cur = self.theme.get(key, "#ffffff")
        chosen = colorchooser.askcolor(color=cur, title=f"Select Color ({key})", parent=self)
        if chosen and chosen[1]:
            hex_val = chosen[1].lower()
            self.theme[key] = hex_val
            if key in self._theme_hex_vars:
                self._theme_hex_vars[key].set(hex_val)
            if key in self._theme_swatch_buttons:
                self._theme_swatch_buttons[key].configure(bg=hex_val, activebackground=hex_val)
            if key == "misora_pink":
                self.theme["misora_pink_hover"] = self._shift_hex(hex_val, 22)
                self.theme["misora_pink_active"] = self._shift_hex(hex_val, -26)
            if hasattr(self, "var_preset"):
                self.var_preset.set(self._detect_active_preset_name())
            self._apply_theme_and_fonts_live(save=True)

    def _commit_theme_hex(self, key: str) -> None:
        hvar = self._theme_hex_vars.get(key)
        if not hvar:
            return
        val = hvar.get().strip()
        if not val.startswith("#"):
            val = "#" + val
        if HEX_COLOR_RE.match(val):
            hex_val = val.lower()
            if self.theme.get(key, "").lower() != hex_val:
                self.theme[key] = hex_val
                if key in self._theme_swatch_buttons:
                    self._theme_swatch_buttons[key].configure(bg=hex_val, activebackground=hex_val)
                if key == "misora_pink":
                    self.theme["misora_pink_hover"] = self._shift_hex(hex_val, 22)
                    self.theme["misora_pink_active"] = self._shift_hex(hex_val, -26)
                if hasattr(self, "var_preset"):
                    self.var_preset.set(self._detect_active_preset_name())
                self._apply_theme_and_fonts_live(save=True)
        else:
            hvar.set(self.theme.get(key, ""))

    def _apply_theme_preset(self, preset_name: str) -> None:
        for key in getattr(self, "_theme_hex_vars", {}):
            self._commit_theme_hex(key)
        if preset_name == "Custom":
            self._apply_theme_and_fonts_live(save=True)
            self.lbl_status.config(text="Applied custom theme colors.")
            self.logger.info("UI / Theme / Config", "Applied custom theme colors.")
            return
        preset = THEME_PRESETS.get(preset_name)
        if not preset:
            return
        self.theme.update(preset)
        if hasattr(self, "var_preset"):
            self.var_preset.set(preset_name)
        for key, hvar in getattr(self, "_theme_hex_vars", {}).items():
            if key in self.theme:
                hvar.set(self.theme[key])
            if key in getattr(self, "_theme_swatch_buttons", {}):
                self._theme_swatch_buttons[key].configure(bg=self.theme[key], activebackground=self.theme[key])
        self._apply_theme_and_fonts_live(save=True)
        self.lbl_status.config(text=f"Applied theme preset: {preset_name}")
        self.logger.info("UI / Theme / Config", f"Applied theme preset '{preset_name}'")

    def _reset_customization_defaults(self) -> None:
        self.prefs["dialogue_font_family"] = DEFAULT_PREFS["dialogue_font_family"]
        self.prefs["dialogue_font_size"] = DEFAULT_PREFS["dialogue_font_size"]
        self.prefs["raw_font_size"] = DEFAULT_PREFS["raw_font_size"]
        self.prefs["ui_font_size"] = DEFAULT_PREFS["ui_font_size"]
        self.theme.clear()
        self.theme.update(DEFAULT_PREFS["theme"])

        if hasattr(self, "var_font_family"):
            self.var_font_family.set(self.prefs["dialogue_font_family"])
            self.var_dlg_font_sz.set(self.prefs["dialogue_font_size"])
            self.var_raw_font_sz.set(self.prefs["raw_font_size"])
            self.var_ui_font_sz.set(self.prefs["ui_font_size"])
            self.var_preset.set("Misora Purple & White")

        for key, hvar in getattr(self, "_theme_hex_vars", {}).items():
            if key in self.theme:
                hvar.set(self.theme[key])
        self._apply_theme_and_fonts_live(save=True)
        self.lbl_status.config(text="Reset display fonts and theme colors to Misora Purple & White default.")
        self.logger.info("UI / Theme / Config", "Reset display fonts and theme colors to default.")

    def _filter_glossary(self) -> None:
        q = self.var_glossary_filter.get().strip().lower()
        if not q:
            self._filtered_glossary_items = list(NGUI_GLOSSARY_ITEMS)
        else:
            self._filtered_glossary_items = [
                item for item in NGUI_GLOSSARY_ITEMS
                if q in item["tag"].lower()
                or q in item["title"].lower()
                or q in item["syntax"].lower()
                or q in item["desc"].lower()
            ]
        self._selected_glossary_idx = 0
        self._render_glossary_list()

    def _render_glossary_list(self) -> None:
        self._glossary_line_map.clear()
        self.txt_glossary.config(state="normal")
        self.txt_glossary.delete("1.0", tk.END)

        line_no = 1
        for idx, item in enumerate(self._filtered_glossary_items):
            sel_tags = ("gl_selected",) if idx == self._selected_glossary_idx else ()
            start_line = line_no

            self.txt_glossary.insert(f"{line_no}.0", f"{item['tag']}  ", ("gl_tag",) + sel_tags)
            self.txt_glossary.insert(f"{line_no}.end", f"{item['title']}\n", ("gl_title",) + sel_tags)
            line_no += 1

            self.txt_glossary.insert(f"{line_no}.0", f"  Example: {item['syntax']}\n", ("gl_syntax",) + sel_tags)
            line_no += 1

            self.txt_glossary.insert(f"{line_no}.0", f"  {item['desc']}\n\n", ("gl_desc",) + sel_tags)
            for ln in range(start_line, line_no + 1):
                self._glossary_line_map[ln] = idx
            line_no += 2

        self.txt_glossary.config(state="disabled")

    def _on_glossary_click(self, event: tk.Event) -> str:
        idx_str = self.txt_glossary.index(f"@{event.x},{event.y}")
        line_no = int(idx_str.split(".")[0])
        item_idx = self._glossary_line_map.get(line_no)
        if item_idx is not None:
            self._selected_glossary_idx = item_idx
            self._render_glossary_list()
        return "break"

    def _on_glossary_double_click(self, event: tk.Event) -> str:
        self._on_glossary_click(event)
        self._insert_selected_glossary_tag()
        return "break"

    def _insert_selected_glossary_tag(self) -> None:
        """Insert or wrap selected dialogue text with the chosen NGUI tag."""
        if not self._filtered_glossary_items:
            return
        idx = max(0, min(self._selected_glossary_idx, len(self._filtered_glossary_items) - 1))
        item = self._filtered_glossary_items[idx]

        if item.get("action") == "ruby":
            self.on_insert_ruby()
            return

        open_tag = item["insert_open"]
        close_tag = item["insert_close"]
        self.apply_ngui_wrapper(open_tag, close_tag)

    def _insert_text_wrapper(self, open_tag: str, close_tag: str, default_inner: str = "") -> None:
        """Wrap the current selection (or insert at caret) in the active dialogue editor."""
        self._current_edit_source = "format"
        try:
            if self.is_box0_active and not self.var_continuous_view.get():
                target = self.txt_box0_summary
                try:
                    sel_first = target.index("sel.first")
                    sel_last = target.index("sel.last")
                    selected_txt = target.get(sel_first, sel_last)
                    target.delete(sel_first, sel_last)
                    target.insert(sel_first, f"{open_tag}{selected_txt}{close_tag}")
                except tk.TclError:
                    target.insert(tk.INSERT, f"{open_tag}{default_inner}{close_tag}")
                self._on_box0_metadata_edited()
                target.focus_set()
                return

            if self.var_continuous_view.get():
                target = self.txt_continuous
                box_idx = self._find_continuous_box_at_index("insert")
                if box_idx is None:
                    self._focus_continuous_box(self.current_box_idx, move_cursor=True)
                try:
                    sel_first = target.index("sel.first")
                    sel_last = target.index("sel.last")
                    b1 = self._find_continuous_box_at_index(sel_first)
                    b2 = self._find_continuous_box_at_index(sel_last)
                    if b1 is not None and b1 == b2:
                        selected_txt = target.get(sel_first, sel_last)
                        target.delete(sel_first, sel_last)
                        target.insert(sel_first, f"{open_tag}{selected_txt}{close_tag}")
                    else:
                        target.insert(tk.INSERT, f"{open_tag}{default_inner}{close_tag}")
                except tk.TclError:
                    target.insert(tk.INSERT, f"{open_tag}{default_inner}{close_tag}")
                self._sync_continuous_box_from_widget()
                target.focus_set()
            else:
                target = self.txt_dialogue
                try:
                    sel_first = target.index("sel.first")
                    sel_last = target.index("sel.last")
                    selected_txt = target.get(sel_first, sel_last)
                    target.delete(sel_first, sel_last)
                    target.insert(sel_first, f"{open_tag}{selected_txt}{close_tag}")
                except tk.TclError:
                    target.insert(tk.INSERT, f"{open_tag}{default_inner}{close_tag}")
                self._on_dialogue_edited()
                target.focus_set()
        finally:
            self._current_edit_source = "keyboard"

    def on_insert_ruby(self) -> None:
        """Open a compact modal prompt to wrap base text with [rub:ruby]base[/rub]."""
        if self.var_preview_compiled.get():
            self.var_preview_compiled.set(False)
            self._update_views()

        selected_base = ""
        if self.var_continuous_view.get():
            target = self.txt_continuous
            try:
                sel_first = target.index("sel.first")
                sel_last = target.index("sel.last")
                b1 = self._find_continuous_box_at_index(sel_first)
                b2 = self._find_continuous_box_at_index(sel_last)
                if b1 is not None and b1 == b2:
                    selected_base = target.get(sel_first, sel_last)
            except tk.TclError:
                pass
        else:
            target = self.txt_dialogue
            try:
                selected_base = target.get("sel.first", "sel.last")
            except tk.TclError:
                pass

        t = self.theme
        panel_fg = best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff")
        editor_fg = best_contrast_fg(t["bg_editor"], t["fg_text"], "#ffffff")

        dlg = tk.Toplevel(self)
        dlg.title("Insert Ruby / Furigana ([rub:...]...[/rub])")
        dlg.configure(bg=t["bg_panel"])
        dlg.resizable(False, False)
        dlg.transient(self)
        dlg.grab_set()

        self.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - 190
        y = self.winfo_rooty() + (self.winfo_height() // 2) - 105
        dlg.geometry(f"380x210+{max(20, x)}+{max(20, y)}")

        tk.Label(
            dlg,
            text="Priconne NGUI Ruby Text ([rub:ruby]base[/rub])",
            font=("Segoe UI", 9, "bold"),
            bg=t["bg_panel"],
            fg=t["misora_pink"],
        ).pack(anchor="w", padx=14, pady=(12, 8))

        row_base = tk.Frame(dlg, bg=t["bg_panel"])
        row_base.pack(fill="x", padx=14, pady=4)
        tk.Label(row_base, text="Base Text (Main):", width=16, anchor="w", bg=t["bg_panel"], fg=panel_fg).pack(side="left")
        var_base = tk.StringVar(master=dlg, value=selected_base)
        ent_base = tk.Entry(
            row_base,
            textvariable=var_base,
            font=("Segoe UI", 10),
            bg=t["bg_editor"],
            fg=editor_fg,
            insertbackground=t["misora_pink"],
            bd=1,
            relief="solid",
            highlightthickness=0,
        )
        ent_base.pack(side="left", fill="x", expand=True)

        row_ruby = tk.Frame(dlg, bg=t["bg_panel"])
        row_ruby.pack(fill="x", padx=14, pady=4)
        tk.Label(row_ruby, text="Ruby Text (Top):", width=16, anchor="w", bg=t["bg_panel"], fg=panel_fg).pack(side="left")
        var_ruby = tk.StringVar(master=dlg)
        ent_ruby = tk.Entry(
            row_ruby,
            textvariable=var_ruby,
            font=("Segoe UI", 10),
            bg=t["bg_editor"],
            fg=editor_fg,
            insertbackground=t["misora_pink"],
            bd=1,
            relief="solid",
            highlightthickness=0,
        )
        ent_ruby.pack(side="left", fill="x", expand=True)

        lbl_preview = tk.Label(
            dlg,
            text=f"Preview: [rub:]{selected_base}[/rub]",
            font=("Consolas", 9),
            bg=t["bg_panel"],
            fg=t["accent_blue"],
            anchor="w",
        )
        lbl_preview.pack(fill="x", padx=14, pady=(8, 10))

        def _update_preview(*_args: Any) -> None:
            lbl_preview.config(text=f"Preview: [rub:{var_ruby.get()}]{var_base.get()}[/rub]")

        var_base.trace_add("write", _update_preview)
        var_ruby.trace_add("write", _update_preview)

        def _safe_close(_event: Optional[tk.Event] = None) -> None:
            safe_grab_release(dlg)
            if dlg.winfo_exists():
                dlg.destroy()

        def _commit(_event: Optional[tk.Event] = None) -> None:
            r_txt = var_ruby.get().strip()
            b_txt = var_base.get()
            _safe_close()
            if not b_txt and not r_txt:
                return
            if selected_base:
                self._insert_text_wrapper(f"[rub:{r_txt}]", "[/rub]")
            else:
                self._insert_text_wrapper(f"[rub:{r_txt}]", "[/rub]", default_inner=b_txt)

        btn_row = tk.Frame(dlg, bg=t["bg_panel"])
        btn_row.pack(fill="x", padx=14, pady=(0, 12))
        ttk.Button(btn_row, text="Cancel", style="TButton", command=_safe_close).pack(side="right", padx=(6, 0))
        ttk.Button(btn_row, text="Insert Ruby Tag", style="Pink.TButton", command=_commit).pack(side="right")

        dlg.protocol("WM_DELETE_WINDOW", _safe_close)
        dlg.bind("<Return>", _commit)
        dlg.bind("<Escape>", _safe_close)
        (ent_ruby if selected_base else ent_base).focus_set()

    _prompt_insert_ruby = on_insert_ruby

    def _highlight_ngui_tags(self) -> None:
        """Apply non-destructive syntax coloring to NGUI & Priconne ruby tags."""
        if self.var_preview_compiled.get():
            return

        self.txt_dialogue.tag_remove("ngui_tag", "1.0", tk.END)
        text = self.txt_dialogue.get("1.0", "end-1c")
        for m in NGUI_TAG_RE.finditer(text):
            self.txt_dialogue.tag_add("ngui_tag", f"1.0 + {m.start()}c", f"1.0 + {m.end()}c")
        self.txt_dialogue.tag_raise("search_hit")

        self.txt_continuous.tag_remove("ngui_tag", "1.0", tk.END)
        if not self.current_doc or not self.current_doc.boxes:
            cont_tx = self.txt_continuous.get("1.0", "end-1c")
            for m in NGUI_TAG_RE.finditer(cont_tx):
                self.txt_continuous.tag_add("ngui_tag", f"1.0 + {m.start()}c", f"1.0 + {m.end()}c")
        else:
            marks = set(self.txt_continuous.mark_names())
            for i in range(len(self.current_doc.boxes)):
                s_mark = f"box_start_{i}"
                e_mark = f"box_end_{i}"
                if s_mark in marks and e_mark in marks:
                    box_tx = self.txt_continuous.get(s_mark, e_mark)
                    for m in NGUI_TAG_RE.finditer(box_tx):
                        self.txt_continuous.tag_add(
                            "ngui_tag",
                            f"{s_mark} + {m.start()}c",
                            f"{s_mark} + {m.end()}c",
                        )
        self.txt_continuous.tag_raise("ngui_tag")
        self.txt_continuous.tag_raise("search_hit")

    def _sync_gd_scroll_bounds(self, _event: Optional[tk.Event] = None) -> None:
        """Keep Game Display canvas width matched to viewport and clamp scrollregion."""
        canvas_w = max(240, self.gd_canvas.winfo_width())
        canvas_h = max(80, self.gd_canvas.winfo_height())
        self.gd_canvas.itemconfigure(self._gd_canvas_win, width=canvas_w)

        req_h = self.gd_inner.winfo_reqheight()
        bound_h = max(req_h, canvas_h)
        self.gd_canvas.configure(scrollregion=(0, 0, canvas_w, bound_h))

        if req_h <= canvas_h:
            self.gd_canvas.yview_moveto(0.0)

    def _on_gd_scrollbar(self, *args: Any) -> None:
        """Scrollbar callback clamped strictly within [0.0, 1.0]."""
        self.gd_canvas.yview(*args)
        top, _ = self.gd_canvas.yview()
        if top < 0.0:
            self.gd_canvas.yview_moveto(0.0)

    def _on_gd_mousewheel(self, event: tk.Event) -> Optional[str]:
        """Smoothly scroll Game Display canvas within bounded upper/lower limits."""
        canvas_h = self.gd_canvas.winfo_height()
        req_h = self.gd_inner.winfo_reqheight()
        if req_h <= canvas_h:
            self.gd_canvas.yview_moveto(0.0)
            return "break"

        delta = -1 if event.delta > 0 else 1
        top, bottom = self.gd_canvas.yview()
        if delta < 0 and top <= 0.0:
            self.gd_canvas.yview_moveto(0.0)
            return "break"
        if delta > 0 and bottom >= 1.0:
            return "break"

        self.gd_canvas.yview_scroll(delta * 2, "units")
        new_top, _ = self.gd_canvas.yview()
        if new_top < 0.0:
            self.gd_canvas.yview_moveto(0.0)
        return "break"

    def _auto_resize_dialogue_box(self) -> None:
        """Adjust dialogue editor line height to fit multi-line text comfortably inside scroll bounds."""
        content = self.txt_dialogue.get("1.0", "end-1c")
        lines = content.split("\n")
        est_visual_lines = sum(max(1, (len(ln) // 68) + 1) for ln in lines)
        target_lines = max(7, min(32, est_visual_lines + 1))
        self.txt_dialogue.configure(height=target_lines)
        self.gd_inner.update_idletasks()
        self._sync_gd_scroll_bounds()

    def _on_toggle_continuous_view(self) -> None:
        """Switch Game Display between Page-by-Page mode and Continuous Dialog Stream with seamless box & caret sync."""
        if self.var_continuous_view.get():
            char_offset = 0
            try:
                target_w = self.txt_box0_summary if self.is_box0_active else self.txt_dialogue
                diff = target_w.count("1.0", "insert", "chars")
                char_offset = max(0, diff[0] if diff else 0)
            except Exception:
                char_offset = 0

            self.gd_scroll_wrap.pack_forget()
            self.continuous_wrap.pack(fill="both", expand=True, padx=8, pady=(0, 6))
            self.lbl_gd_title.config(text="GAME VIEW (Continuous Stream)")
            self._update_views()
            target_idx = -1 if self.is_box0_active else self.current_box_idx
            self.after(50, lambda: self._focus_continuous_box(target_idx, move_cursor=True, char_offset=char_offset))
        else:
            # 1. Flush any uncommitted card edits
            self._flush_continuous_card_edits()

            # 2. Extract char offset from active card's text editor
            char_offset = 0
            active_idx = -1 if getattr(self, "is_box0_active", False) else self.current_box_idx
            if hasattr(self, "_card_widgets") and active_idx in self._card_widgets:
                try:
                    txt_w = self._card_widgets[active_idx].get("txt")
                    if txt_w:
                        diff = txt_w.count("1.0", "insert", "chars")
                        char_offset = max(0, diff[0] if diff else 0)
                except Exception:
                    char_offset = 0
            elif hasattr(self, "txt_continuous"):
                try:
                    diff = self.txt_continuous.count("1.0", "insert", "chars")
                    char_offset = max(0, diff[0] if diff else 0)
                except Exception:
                    char_offset = 0

            self.continuous_wrap.pack_forget()
            self.gd_scroll_wrap.pack(fill="both", expand=True, padx=4, pady=(0, 4))
            self.lbl_gd_title.config(text="GAME VIEW (Clean Dialogue)")
            self._update_views()

            try:
                target_w = self.txt_box0_summary if self.is_box0_active else self.txt_dialogue
                target_w.mark_set("insert", f"1.0 + {max(0, char_offset)}c")
                target_w.see("insert")
                target_w.focus_set()
            except Exception:
                pass

    # -------------------------------------------------------------------------
    # Status & Action Bar
    # -------------------------------------------------------------------------
    def _build_status_bar(self) -> None:
        t = self.theme
        action_bar = self._tag_role(
            tk.Frame(self, bg=t["bg_panel"], bd=1, relief="solid", highlightbackground=t["border"], highlightthickness=1),
            "panel_box"
        )
        action_bar.pack(fill="x", padx=8, pady=(0, 6))

        self.lbl_status = self._tag_role(
            tk.Label(action_bar, text=getattr(self, "_default_status_text", "Ready. Drag & Drop or open a .unity3d bundle or folder to begin."), font=("Segoe UI", 9), bg=t["bg_panel"], fg=t["fg_muted"]),
            "label_muted"
        )
        self.lbl_status.pack(side="left", padx=8, pady=6)

        self.var_sync_xuat = tk.BooleanVar(master=self, value=True)
        cb_sync = ttk.Checkbutton(
            action_bar,
            text="Also update matching XUAT .txt dictionary on Save",
            variable=self.var_sync_xuat,
            style="Panel.TCheckbutton"
        )
        cb_sync.pack(side="right", padx=(8, 12))

        self.ico_revert = self.get_icon("revert", (15, 15))
        btn_revert = ttk.Button(action_bar, text=" Revert Box", image=self.ico_revert, compound="left", style="TButton", command=self.on_revert_box)
        btn_revert.pack(side="right", padx=4)

        self.ico_save = self.get_icon("save", (15, 15))
        self.btn_save = ttk.Button(action_bar, text=" Save & Patch Bundle (Ctrl+S)", image=self.ico_save, compound="left", style="Pink.TButton", command=self.on_save)
        self.btn_save.pack(side="right", padx=4)

    def _toggle_console_shortcut(self) -> None:
        """Inform user that diagnostic logs stream live to the standard Windows console."""
        self.show_toast("Logs stream to the persistent Windows console.")

    def _get_active_text_widget(self) -> Optional[tk.Text]:
        """Resolve the currently active or focused Text widget safely without aliasing (Rule 3)."""
        focused = self.focus_get()
        if isinstance(focused, tk.Text):
            return focused
        if getattr(self, "var_continuous_view", None) and self.var_continuous_view.get():
            if getattr(self, "is_box0_active", False) and hasattr(self, "_card_widgets") and -1 in self._card_widgets:
                card_txt = self._card_widgets[-1].get("txt")
                if card_txt and card_txt.winfo_exists():
                    return card_txt
            if hasattr(self, "_card_widgets") and self.current_box_idx in self._card_widgets:
                card_txt = self._card_widgets[self.current_box_idx].get("txt")
                if card_txt and card_txt.winfo_exists():
                    return card_txt
            if hasattr(self, "txt_continuous") and self.txt_continuous.winfo_exists():
                return self.txt_continuous
        if getattr(self, "is_box0_active", False) and hasattr(self, "txt_box0_summary") and self.txt_box0_summary.winfo_exists():
            return self.txt_box0_summary
        if hasattr(self, "txt_dialogue") and self.txt_dialogue.winfo_exists():
            return self.txt_dialogue
        return getattr(self, "txt_dialogue", None)

    def _get_card_text_widget(self, box_idx: int) -> "tk.Text":
        """Return the card Text widget for box_idx if it exists, else txt_dialogue fallback (S4).

        Guards with winfo_exists() before returning the card widget to avoid stale references
        (STALE-CARD-REGISTRY / Rule 3 widget aliasing guard).
        """
        if hasattr(self, "_card_widgets") and box_idx in self._card_widgets:
            w = self._card_widgets[box_idx].get("txt")
            if w is not None:
                try:
                    if w.winfo_exists():
                        return w
                except Exception:
                    pass
        return self.txt_dialogue

    def _install_shortcuts_bindtag(self, widget: tk.Widget) -> None:
        """Install MisoraShortcuts as the FIRST bindtag on an editor widget (Rule 12)."""
        try:
            current_tags = list(widget.bindtags())
            if "MisoraShortcuts" not in current_tags:
                widget.bindtags(("MisoraShortcuts",) + tuple(current_tags))
        except Exception:
            pass

    def _on_misora_shortcut(self, event: tk.Event) -> Optional[str]:
        """Central shortcut dispatcher on the MisoraShortcuts bindtag (Rule 12)."""
        # 1. Skip if modal grab is active (unless it's self)
        current_grab = self.grab_current()
        if current_grab is not None and current_grab != self:
            return None

        # 2. Skip IME composition / dead keys / empty keysyms
        keysym = getattr(event, "keysym", "")
        if not keysym or keysym.startswith("dead_") or keysym in ("Next_Virtual_Key", "VoidSymbol"):
            return None

        key_lower = keysym.lower()
        state = getattr(event, "state", 0)

        # Modifier bitmasks (Windows Tkinter standard):
        # Shift: 0x0001
        # CapsLock: 0x0002 (mask out)
        # Control: 0x0004
        # Alt: 0x0008 (Mod1) or 0x0020 (Mod3)
        # NumLock: 0x0100 (mask out)
        is_shift = bool(state & 0x0001)
        is_ctrl = bool(state & 0x0004)
        is_alt = bool((state & 0x0008) or (state & 0x0020))

        # 3. Protect against AltGr (Ctrl+Alt)
        if is_ctrl and is_alt:
            return None

        # 4. Standard Ctrl+C / Ctrl+X / Ctrl+A: let native widget handlers process them
        if is_ctrl and not is_shift and not is_alt:
            if key_lower in ("c", "x", "a"):
                return None

        # 5. Ctrl+V in editor widget: CSIF detection
        if is_ctrl and not is_shift and not is_alt and key_lower == "v":
            clip_text = self.safe_clipboard_get()
            if clip_text and sniff_format(clip_text) == "csif":
                w = event.widget if isinstance(event.widget, tk.Widget) else self._get_active_text_widget()
                self._handle_editor_csif_paste(w, clip_text)
                return "break"
            return None  # Let standard paste proceed

        # 6. Whitelisted Application Shortcuts (return "break" on match)
        if is_ctrl and not is_alt:
            if not is_shift:
                if key_lower == "h":
                    self.on_show_replace()
                    return "break"
                elif key_lower == "s":
                    self.on_save()
                    return "break"
                elif key_lower == "o":
                    self.on_open_file()
                    return "break"
                elif key_lower == "f":
                    self.on_show_find()
                    return "break"
                elif key_lower == "n":
                    self.on_box_new()
                    return "break"
                elif key_lower == "z":
                    self.on_undo()
                    return "break"
                elif key_lower == "y":
                    self.on_redo()
                    return "break"
                elif key_lower == "t":
                    self.on_copy_ai_prompt()
                    return "break"
                elif key_lower == "b":
                    self._shortcut_wrap("[b]", "[/b]")
                    return "break"
                elif key_lower == "i":
                    self._shortcut_wrap("[i]", "[/i]")
                    return "break"
                elif key_lower == "u":
                    self._shortcut_wrap("[u]", "[/u]")
                    return "break"
                elif key_lower == "p":
                    self.on_insert_playername()
                    return "break"
                elif key_lower == "l":
                    self.on_toggle_lock_current_box()
                    return "break"
            else:  # is_shift
                if key_lower == "z":
                    self.on_redo()
                    return "break"
                elif key_lower == "c":
                    self.on_copy_script()
                    return "break"
                elif key_lower == "v":
                    self.on_paste_cross_box()
                    return "break"
                elif key_lower == "t":
                    self.on_copy_ai_prompt()
                    return "break"
                elif key_lower == "i":
                    self.on_import_script()
                    return "break"
                elif key_lower == "e":
                    self.on_export_script()
                    return "break"

        return None

    def _show_csif_paste_chooser(self, clip_text: str) -> Optional[str]:
        """Display modal 4-way chooser dialog when CSIF content is pasted into an editor (Part C.4)."""
        t = self.theme
        dlg = tk.Toplevel(self)
        dlg.title("CSIF Script Detected")
        dlg.transient(self)
        dlg.resizable(False, False)
        dlg.configure(bg=t["bg_panel"])

        choice: List[Optional[str]] = [None]

        def _choose(val: Optional[str]) -> None:
            choice[0] = val
            try:
                dlg.grab_release()
            except Exception:
                pass
            dlg.destroy()

        parsed = parse(clip_text)
        block_count = len(parsed.blocks)
        first_sp = ", ".join(
            (b.speaker if b.speaker else "Narration") for b in parsed.blocks[:3]
        )
        if block_count > 3:
            first_sp += f", ... (+{block_count - 3} more)"

        frame = tk.Frame(dlg, bg=t["bg_panel"], padx=16, pady=14)
        frame.pack(fill="both", expand=True)

        lbl_hdr = tk.Label(
            frame,
            text="Misora CSIF Script Detected in Clipboard",
            font=("Segoe UI", 11, "bold"),
            fg=t["misora_pink"],
            bg=t["bg_panel"],
        )
        lbl_hdr.pack(anchor="w", pady=(0, 6))

        info_txt = (
            f"The clipboard contains {block_count} structured dialogue block(s).\n"
            f"Speakers: {first_sp}\n\n"
            f"Please choose how you would like to apply this clipboard content:"
        )
        lbl_info = tk.Label(
            frame,
            text=info_txt,
            font=("Segoe UI", 9),
            fg=t["fg_text"],
            bg=t["bg_panel"],
            justify="left",
        )
        lbl_info.pack(anchor="w", pady=(0, 12))

        btn_box = tk.Frame(frame, bg=t["bg_panel"])
        btn_box.pack(fill="x", pady=(4, 0))

        btn_ins = tk.Button(
            btn_box,
            text="📥 Insert as New Boxes",
            font=("Segoe UI", 9, "bold"),
            bg=t["highlight_bg"],
            fg=best_contrast_fg(t["highlight_bg"]),
            relief="raised",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: _choose("insert"),
        )
        btn_ins.pack(fill="x", pady=2)

        btn_rep = tk.Button(
            btn_box,
            text="🔄 Paste Across Boxes (Replace)",
            font=("Segoe UI", 9),
            bg=t["bg_editor"],
            fg=t["fg_text"],
            relief="raised",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: _choose("replace"),
        )
        btn_rep.pack(fill="x", pady=2)

        btn_txt = tk.Button(
            btn_box,
            text="📝 Paste as Plain Text",
            font=("Segoe UI", 9),
            bg=t["bg_editor"],
            fg=t["fg_text"],
            relief="raised",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: _choose("text"),
        )
        btn_txt.pack(fill="x", pady=2)

        btn_cancel = tk.Button(
            btn_box,
            text="❌ Cancel",
            font=("Segoe UI", 9),
            bg=t["bg_panel"],
            fg=t["fg_muted"],
            relief="groove",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: _choose(None),
        )
        btn_cancel.pack(fill="x", pady=(4, 0))

        dlg.bind("<Escape>", lambda e: _choose(None))
        dlg.protocol("WM_DELETE_WINDOW", lambda: _choose(None))

        dlg.update_idletasks()
        try:
            pw = self.winfo_width()
            ph = self.winfo_height()
            px = self.winfo_rootx()
            py = self.winfo_rooty()
            dw = dlg.winfo_width()
            dh = dlg.winfo_height()
            dlg.geometry(f"+{px + max(0, (pw - dw) // 2)}+{py + max(0, (ph - dh) // 2)}")
        except Exception:
            pass

        try:
            dlg.grab_set()
            dlg.focus_set()
            self.wait_window(dlg)
        except Exception:
            pass

        return choice[0]

    def _handle_editor_csif_paste(self, widget: tk.Widget, clip_text: str) -> None:
        """Show 4-way chooser dialog when CSIF content is pasted into an editor (Part C.4)."""
        res = self._show_csif_paste_chooser(clip_text)
        if res == "insert":
            self.on_box_paste(confirm=False)
        elif res == "replace":
            self.on_paste_cross_box()
        elif res == "text":
            if isinstance(widget, tk.Text) and widget.winfo_exists():
                try:
                    sel = widget.tag_ranges("sel")
                    if sel:
                        widget.delete(sel[0], sel[1])
                except Exception:
                    pass
                widget.insert(tk.INSERT, clip_text)
                self._commit_widget_edit(widget)

    def _bind_shortcuts(self) -> None:
        self.bind_class("MisoraShortcuts", "<KeyPress>", self._on_misora_shortcut)
        for w in (
            getattr(self, "txt_dialogue", None),
            getattr(self, "entry_speaker", None),
            getattr(self, "txt_continuous", None),
            getattr(self, "txt_box0_summary", None),
            getattr(self, "entry_box0_title", None),
            getattr(self, "entry_box0_subtitle", None),
        ):
            if w is not None:
                self._install_shortcuts_bindtag(w)

        self.bind("<Control-o>", lambda e: self.on_open_file())
        self.bind("<Control-O>", lambda e: self.on_open_folder())
        self.bind("<Control-s>", lambda e: self.on_save())
        self.bind("<Control-q>", lambda e: self._on_app_exit())
        self.bind("<Control-r>", lambda e: self.on_insert_ruby())
        self.bind("<Control-p>", lambda e: self.on_insert_playername())
        self.bind_all("<Control-f>", lambda e: self.on_show_find())
        self.bind_all("<Control-F>", lambda e: self.on_show_find_in_files())
        self.bind_all("<Control-h>", lambda e: self.on_show_replace())
        self.bind("<Control-z>", lambda e: self.on_undo())
        self.bind("<Control-y>", lambda e: self.on_redo())
        self.bind("<Control-Shift-Z>", lambda e: self.on_redo())
        self.bind("<Control-Shift-z>", lambda e: self.on_redo())
        self.bind("<Control-C>", lambda e: self._toggle_continuous_shortcut())
        self.bind("<Control-comma>", lambda e: self._toggle_side_drawer("customize"))
        self.bind("<F1>", lambda e: self._toggle_side_drawer("glossary"))
        self.bind("<F5>", lambda e: self.on_reload())
        self.bind("<F9>", lambda e: self.on_launch_datamine())
        self.bind("<F12>", lambda e: self._toggle_console_shortcut())
        self.bind("<Alt-Left>", lambda e: self.on_prev_box())
        self.bind("<Alt-Right>", lambda e: self.on_next_box())
        self.bind("<Alt-Up>", lambda e: self.on_prev_box())
        self.bind("<Alt-Down>", lambda e: self.on_next_box())
        self.bind("<Control-t>", lambda e: self.on_open_translator_assistant())
        self.bind("<Control-T>", lambda e: self.on_copy_ai_prompt())
        self.bind("<Control-Shift-T>", lambda e: self.on_copy_ai_prompt())
        self.bind("<Control-Shift-t>", lambda e: self.on_copy_ai_prompt())
        self.bind("<Control-Shift-C>", lambda e: self.on_copy_script())
        self.bind("<Control-Shift-c>", lambda e: self.on_copy_script())
        self.bind("<Control-Shift-V>", lambda e: self.on_paste_cross_box())
        self.bind("<Control-Shift-v>", lambda e: self.on_paste_cross_box())
        self.bind("<Control-Shift-I>", lambda e: self.on_import_script())
        self.bind("<Control-Shift-i>", lambda e: self.on_import_script())
        self.bind("<Control-Shift-E>", lambda e: self.on_export_script())
        self.bind("<Control-Shift-e>", lambda e: self.on_export_script())
        self.bind("<Control-l>", lambda e: self.on_toggle_lock_current_box())
        self.bind("<Control-L>", lambda e: self.on_toggle_lock_current_box())
        self.bind("<F8>", lambda e: self.on_translate_current_box())

    def _toggle_continuous_shortcut(self) -> None:
        self.var_continuous_view.set(not self.var_continuous_view.get())
        self._on_toggle_continuous_view()

    # -------------------------------------------------------------------------
    # Document Loading & Box Display (Page Mode + Continuous Stream Mode)
    # -------------------------------------------------------------------------
    def _flush_active_widget(self) -> bool:
        """Explicitly resolve the active editor widget and commit any pending edits (S1/S3).

        Returns True if flushed cleanly or no active widget, False on commit failure.
        """
        if getattr(self, "current_file_path", None) is None:
            return True

        widget = None
        is_cont = bool(getattr(self, "var_continuous_view", None) and self.var_continuous_view.get())
        cards = getattr(self, "_card_widgets", {})

        if is_cont:
            if getattr(self, "is_box0_active", False) and -1 in cards:
                candidate = cards[-1].get("txt")
                if candidate is not None and candidate.winfo_exists():
                    widget = candidate
            elif getattr(self, "current_box_idx", -1) in cards:
                candidate = cards[self.current_box_idx].get("txt")
                if candidate is not None and candidate.winfo_exists():
                    widget = candidate
            elif getattr(self, "current_doc", None) is None:
                candidate = getattr(self, "txt_continuous", None)
                if candidate is not None and candidate.winfo_exists():
                    widget = candidate
        else:
            if getattr(self, "is_box0_active", False):
                candidate = getattr(self, "txt_box0_summary", None)
                if candidate is not None and candidate.winfo_exists():
                    widget = candidate
            else:
                candidate = getattr(self, "txt_dialogue", None)
                if candidate is not None and candidate.winfo_exists():
                    widget = candidate

        if widget is not None:
            try:
                self._commit_widget_edit(widget)
            except Exception as e:
                self.logger.exception("Failed to flush pending edit:", e)
                messagebox.showerror("Edit Commit Error", f"Could not preserve the current edit:\n{e}")
                return False

        try:
            if hasattr(self, "focus_get") and self.focus_get() == getattr(self, "entry_speaker", None):
                self._commit_speaker_edit()
        except Exception:
            pass
        return True

