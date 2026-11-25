# misora.py PART 05/12 | ORIG L5666-L7163/17315 | SHA:ec4d9bfc8ec6
# SYMS: L5666:MisoraApp._on_toggle_line_numbers, L5719:MisoraApp._on_toggle_column_ruler, L5751:MisoraApp._update_gutter_clean, L5766:MisoraApp._sync_continuous_gutter_scroll, L5774:MisoraApp._on_continuous_vscroll, L5783:MisoraApp._highlight_secret_whitespace, L5793:MisoraApp._shortcut_wrap, L5797:MisoraApp._shortcut_undo, L5801:MisoraApp._shortcut_redo, L5805:MisoraApp._set_ribbon_colors, L5816:MisoraApp._apply_active_ribbon_color, L5820:MisoraApp._apply_active_ribbon_gradient, L5825:MisoraApp.on_open_color_picker, L5840:MisoraApp.apply_ngui_wrapper, L5854:MisoraApp._update_top_header_title, L5866:MisoraApp._on_toggle_ngui_ribbon, L5879:MisoraApp._on_dialogue_preview_configure, L5890:MisoraApp._hide_dialogue_preview_and_restore_editor, L5901:MisoraApp._render_dialogue_preview_frame, L6002:MisoraApp._on_toggle_preview_compiled, L6060:MisoraApp._get_or_create_compiled_style_tag, L6096:MisoraApp._insert_compiled_ngui_text, L6234:MisoraApp._build_side_drawer, L6298:MisoraApp._build_customize_tab, L6455:MisoraApp._build_glossary_tab, L6527:MisoraApp._open_side_drawer, L6533:MisoraApp._close_side_drawer, L6538:MisoraApp._toggle_side_drawer, L6544:MisoraApp._switch_side_drawer_tab, L6572:MisoraApp._on_font_pref_changed, L6599:MisoraApp._adjust_dialogue_font_size, L6607:MisoraApp._pick_theme_color, L6624:MisoraApp._commit_theme_hex, L6646:MisoraApp._apply_theme_preset, L6669:MisoraApp._reset_customization_defaults, L6691:MisoraApp._filter_glossary, L6706:MisoraApp._render_glossary_list, L6730:MisoraApp._on_glossary_click, L6739:MisoraApp._on_glossary_double_click, L6744:MisoraApp._insert_selected_glossary_tag, L6759:MisoraApp._insert_text_wrapper, L6823:MisoraApp.on_insert_ruby, L6964:MisoraApp._highlight_ngui_tags, L6997:MisoraApp._sync_gd_scroll_bounds, L7010:MisoraApp._on_gd_scrollbar, L7017:MisoraApp._on_gd_mousewheel, L7039:MisoraApp._auto_resize_dialogue_box, L7049:MisoraApp._on_toggle_continuous_view, L7107:MisoraApp._build_status_bar, L7138:MisoraApp._toggle_console_shortcut, L7142:MisoraApp._get_active_text_widget

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
        self._redraw_pixel_rulers()
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
        if visible:
            self._redraw_pixel_rulers()
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
            self._apply_gutter_overflow_tag(self.gutter_clean)
            self.gutter_clean.config(state="disabled")
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

    def apply_ngui_wrapper(self, open_tag: str, close_tag: str, default_inner: str = "") -> None:
        """Ensure Raw Edit mode is active, then wrap selection or insert NGUI tags at caret."""
        if not getattr(self, "is_box0_active", False) and self.current_doc and self.is_box_locked(self.current_box_idx):
            self.show_toast(f"Box #{self.current_box_idx + 1} is locked.")
            return

        if self.var_preview_compiled.get():
            self.var_preview_compiled.set(False)
            self._update_views()
        self._insert_text_wrapper(open_tag, close_tag, default_inner=default_inner)
        target = self._get_active_text_widget()
        if target:
            self._commit_widget_edit(target)

    def _update_top_header_title(self) -> None:
        """Update top view header title according to active view and preview modes (FEAT-03)."""
        if not hasattr(self, "lbl_gd_title"):
            return
        is_cont = bool(getattr(self, "var_continuous_view", None) and self.var_continuous_view.get())
        is_prev = bool(getattr(self, "var_preview_compiled", None) and self.var_preview_compiled.get())
        if is_cont:
            title = "All Script Preview" if is_prev else "All Script"
        else:
            title = "Dialogue Preview" if is_prev else "Dialogue"
        self.lbl_gd_title.config(text=title)

    def _on_toggle_ngui_ribbon(self) -> None:
        """Toggle visibility of the NGUI formatting ribbon docked in ribbon_actions_row (FEAT-04)."""
        if not hasattr(self, "ribbon_frame"):
            return
        if self.var_show_ngui_ribbon.get():
            if hasattr(self, "actions_bar") and self.actions_bar.winfo_manager():
                self.ribbon_frame.pack(side="left", padx=(0, 4), before=self.actions_bar)
            else:
                self.ribbon_frame.pack(side="left", padx=(0, 4))
        else:
            self.ribbon_frame.pack_forget()
        self._save_user_prefs(silent=True)

    def _on_dialogue_preview_configure(self, event: Optional[tk.Event] = None) -> None:
        """Keep Dialogue Preview scrollregion synced on resize without accumulating canvas items."""
        if not hasattr(self, "dialogue_preview_canvas") or not self.dialogue_preview_canvas.winfo_exists():
            return
        try:
            bbox = self.dialogue_preview_canvas.bbox("all")
            if bbox:
                self.dialogue_preview_canvas.configure(scrollregion=bbox)
        except Exception:
            pass

    def _hide_dialogue_preview_and_restore_editor(self) -> None:
        """Hide Dialogue Preview canvas and restore ruler_clean above clean_editor_row in exact pack order."""
        if hasattr(self, "dialogue_preview_canvas") and self._is_widget_packed(self.dialogue_preview_canvas):
            self.dialogue_preview_canvas.pack_forget()
        if hasattr(self, "clean_editor_row") and not self._is_widget_packed(self.clean_editor_row):
            if self.show_column_ruler and hasattr(self, "ruler_clean"):
                if self._is_widget_packed(self.ruler_clean):
                    self.ruler_clean.pack_forget()
                self.ruler_clean.pack(side="top", fill="x", pady=(0, 2))
            self.clean_editor_row.pack(fill="both", expand=True)

    def _render_dialogue_preview_frame(self, speaker: str, raw_text: str) -> None:
        """Render code-drawn Priconne-style dialogue frame on single Canvas + embedded read-only Text."""
        if not hasattr(self, "dialogue_preview_canvas") or not self.dialogue_preview_canvas.winfo_exists():
            return

        canvas = self.dialogue_preview_canvas
        txt_w = self.txt_dialogue_preview
        t = self.theme
        d_fam = getattr(self, "dialogue_font_family", self.prefs.get("dialogue_font_family", "Consolas"))
        d_sz = int(getattr(self, "dialogue_font_size", self.prefs.get("dialogue_font_size", 11)))

        canvas.configure(bg=t["bg_panel"])
        canvas.delete("preview_frame")

        metrics = self._measure_dialogue_metrics(raw_text)
        f = self._get_dialogue_measure_font()
        safe_w = metrics["safe_w"]
        line_h = max(16, int(f.metrics("linespace") or 18) + 4)
        safe_h = line_h * 3

        pad_x = 14
        pad_y = 10
        frame_x = 12
        frame_y = 26
        frame_w = safe_w + pad_x * 2
        frame_h = safe_h + pad_y * 2

        cream_bg = "#fffcf4"
        outer_gold = "#d4af37"
        inner_gold = "#e6c875"
        plate_bg = "#3b2c4e"
        plate_fg = best_contrast_fg(plate_bg, "#ffffff", "#fffcf4")
        text_fg = best_contrast_fg(cream_bg, "#2b2118", "#1a1a1a")
        arrow_fg = "#ff5c93"

        # Priconne-style double border (pure Tk Canvas primitives, zero AtlasAdv sprites)
        canvas.create_rectangle(
            frame_x, frame_y, frame_x + frame_w, frame_y + frame_h,
            fill=cream_bg, outline=outer_gold, width=2, tags="preview_frame",
        )
        canvas.create_rectangle(
            frame_x + 4, frame_y + 4, frame_x + frame_w - 4, frame_y + frame_h - 4,
            fill="", outline=inner_gold, width=1, tags="preview_frame",
        )

        # Name plate
        sp_label = speaker.strip() if speaker and speaker.strip() else "(Narration)"
        plate_w = max(96, int(f.measure(sp_label)) + 24)
        plate_x1 = frame_x + 12
        plate_y1 = frame_y - 14
        plate_x2 = plate_x1 + plate_w
        plate_y2 = frame_y + 10
        canvas.create_rectangle(
            plate_x1, plate_y1, plate_x2, plate_y2,
            fill=plate_bg, outline=outer_gold, width=1, tags="preview_frame",
        )
        canvas.create_text(
            (plate_x1 + plate_x2) // 2, (plate_y1 + plate_y2) // 2,
            text=sp_label, fill=plate_fg, font=(d_fam, max(8, d_sz - 1), "bold"),
            tags="preview_frame",
        )

        # Static pink ▼ indicator at bottom-right of calibrated safe frame
        canvas.create_text(
            frame_x + frame_w - 14, frame_y + frame_h - 12,
            text="▼", fill=arrow_fg, font=(d_fam, max(8, d_sz - 2), "bold"),
            tags="preview_frame",
        )

        # Size embedded Text so >50d lines and 4+ lines visibly bleed past the calibrated frame
        max_px = max(safe_w, max((ln["pixel_width"] for ln in metrics["lines"]), default=0))
        line_cnt = max(3, metrics["line_count"])
        win_w = max_px + 24
        txt_x = frame_x + pad_x
        txt_y = frame_y + pad_y

        txt_w.config(state="normal")
        txt_w.configure(
            wrap="none",
            height=line_cnt,
            font=(d_fam, d_sz),
            bg=cream_bg,
            fg=text_fg,
            selectbackground=t["highlight_bg"],
            selectforeground=t["misora_pink"],
        )
        txt_w.delete("1.0", tk.END)
        self._configure_editor_rich_tags(txt_w, d_fam, d_sz)
        self._insert_compiled_ngui_text(txt_w, "1.0", raw_text)
        self._apply_overflow_highlights(txt_w)
        txt_w.config(state="disabled")

        canvas.coords(self._dialogue_preview_win, txt_x, txt_y)
        canvas.itemconfigure(self._dialogue_preview_win, width=win_w)
        canvas.tag_raise(self._dialogue_preview_win)
        canvas.tag_raise("preview_frame")

        total_w = max(frame_x + frame_w + 16, txt_x + win_w + 12)
        total_h = max(frame_y + frame_h + 16, txt_y + line_cnt * line_h + 16)
        canvas.configure(width=total_w, height=total_h, scrollregion=(0, 0, total_w, total_h))

    def _on_toggle_preview_compiled(self) -> None:
        """Toggle between editable raw NGUI tags and compiled visual preview."""
        if self.var_preview_compiled.get():
            if hasattr(self, "txt_dialogue") and self.txt_dialogue.winfo_exists():
                try:
                    caret = self.txt_dialogue.index("insert")
                except tk.TclError:
                    caret = "1.0"
                try:
                    sel_range = (
                        self.txt_dialogue.index("sel.first"),
                        self.txt_dialogue.index("sel.last"),
                    )
                except tk.TclError:
                    sel_range = None
                try:
                    y_top = float(self.txt_dialogue.yview()[0])
                except Exception:
                    y_top = 0.0
                self._preview_saved_editor_state = (
                    self.current_file_path,
                    self.current_box_idx,
                    getattr(self, "is_box0_active", False),
                    caret,
                    sel_range,
                    y_top,
                )
            self.lbl_status.config(
                text="Compiled Attribute Preview ON (read-only) — uncheck 'Compiled' to edit raw tags."
            )
        else:
            self.lbl_status.config(
                text="Raw NGUI Tag Edit Mode active."
            )
        self._update_top_header_title()
        self._update_views()

        if not self.var_preview_compiled.get():
            saved = getattr(self, "_preview_saved_editor_state", None)
            self._preview_saved_editor_state = None
            if (
                saved
                and hasattr(self, "txt_dialogue")
                and self.txt_dialogue.winfo_exists()
                and saved[0] == self.current_file_path
                and saved[1] == self.current_box_idx
                and saved[2] == getattr(self, "is_box0_active", False)
            ):
                _, _, _, caret, sel_range, y_top = saved
                try:
                    self.txt_dialogue.mark_set("insert", caret)
                    if sel_range:
                        self.txt_dialogue.tag_remove("sel", "1.0", tk.END)
                        self.txt_dialogue.tag_add("sel", sel_range[0], sel_range[1])
                    self.txt_dialogue.yview_moveto(y_top)
                except tk.TclError:
                    pass

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
        d_fam = getattr(self, "dialogue_font_family", self.prefs.get("dialogue_font_family", "Consolas"))
        d_sz = int(getattr(self, "dialogue_font_size", self.prefs.get("dialogue_font_size", 11)))
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

        self.btn_tab_mtl = ttk.Button(
            drawer_top,
            text="MTL",
            style="TButton",
            command=lambda: self._switch_side_drawer_tab("mtl"),
        )
        self.btn_tab_mtl.pack(side="left", padx=(4, 0))
        create_tooltip(self.btn_tab_mtl, "Machine Translation Drawer (Ctrl+T)")

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

        self.tab_mtl_frame = self._tag_role(tk.Frame(self.side_drawer, bg=t["bg_panel"]), "panel")
        self._build_mtl_tab(self.tab_mtl_frame)

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
        for frame in (
            getattr(self, "tab_customize_frame", None),
            getattr(self, "tab_glossary_frame", None),
            getattr(self, "tab_mtl_frame", None),
        ):
            if frame is not None:
                frame.pack_forget()
        for btn in (
            getattr(self, "btn_tab_customize", None),
            getattr(self, "btn_tab_glossary", None),
            getattr(self, "btn_tab_mtl", None),
        ):
            if btn is not None:
                btn.configure(style="TButton")

        if tab == "customize":
            self.tab_customize_frame.pack(fill="both", expand=True)
            self.btn_tab_customize.configure(style="Pink.TButton")
        elif tab == "mtl":
            self.tab_mtl_frame.pack(fill="both", expand=True)
            self.btn_tab_mtl.configure(style="Pink.TButton")
            self._refresh_mtl_drawer_box()
        else:
            self.tab_glossary_frame.pack(fill="both", expand=True)
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
                if hasattr(self, "_card_widgets") and self.current_box_idx in self._card_widgets:
                    target = self._get_card_text_widget(self.current_box_idx)
                    try:
                        sel_first = target.index("sel.first")
                        sel_last = target.index("sel.last")
                        selected_txt = target.get(sel_first, sel_last)
                        target.delete(sel_first, sel_last)
                        target.insert(sel_first, f"{open_tag}{selected_txt}{close_tag}")
                    except tk.TclError:
                        target.insert(tk.INSERT, f"{open_tag}{default_inner}{close_tag}")
                    target.focus_set()
                else:
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
                target.focus_set()
        finally:
            self._current_edit_source = "keyboard"

    def on_insert_ruby(self) -> None:
        """Open a compact modal prompt to wrap base text with [rub:ruby]base[/rub]."""
        if not getattr(self, "is_box0_active", False) and self.current_doc and self.is_box_locked(self.current_box_idx):
            self.show_toast(f"Box #{self.current_box_idx + 1} is locked.")
            return

        if self.var_preview_compiled.get():
            self.var_preview_compiled.set(False)
            self._update_views()

        selected_base = ""
        if self.var_continuous_view.get():
            if hasattr(self, "_card_widgets") and self.current_box_idx in self._card_widgets:
                target = self._get_card_text_widget(self.current_box_idx)
                try:
                    selected_base = target.get("sel.first", "sel.last")
                except tk.TclError:
                    pass
            else:
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
            target = self._get_active_text_widget()
            if target:
                self._commit_widget_edit(target)

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
        self._apply_overflow_highlights(self.txt_dialogue)
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
            self._update_top_header_title()
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
            self._update_top_header_title()
            self._update_views()

            try:
                target_w = self.txt_box0_summary if self.is_box0_active else self.txt_dialogue
                target_w.mark_set("insert", f"1.0 + {max(0, char_offset)}c")
                target_w.see("insert")
                target_w.focus_set()
            except Exception:
                pass

        if hasattr(self, "_set_mtl_drawer_mode"):
            self._set_mtl_drawer_mode("all_script" if self.var_continuous_view.get() else "dialogue")

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

