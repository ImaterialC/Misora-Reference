# ======================================================================
# FILE: misora.py — PART 07 / 10
# ORIGINAL LINE RANGE : L7934 .. L9396 (total 1463 lines of 12835)
# SOURCE SHA-256      : d23baae2be82fe93a18da7d3769af30d19ebe02a8b5f6a3645d56a6f53c0710e
# NOTE FOR AI REVIEWER: Cite ORIGINAL line numbers (L7934..L9396) and symbol names.
# SYMBOLS IN THIS PART (with exact original line numbers):
#   L07934:   MisoraApp._render_continuous_view (def)
#   L08199:   MisoraApp._focus_continuous_box (def)
#   L08253:   MisoraApp._find_continuous_box_at_index (def)
#   L08259:   MisoraApp._nearest_continuous_box_to_index (def)
#   L08263:   MisoraApp._on_continuous_cursor_moved (def)
#   L08267:   MisoraApp._on_continuous_key_guard (def)
#   L08271:   MisoraApp._on_continuous_copy (def)
#   L08275:   MisoraApp._on_continuous_paste_guard (def)
#   L08279:   MisoraApp._on_continuous_cut_guard (def)
#   L08283:   MisoraApp._on_continuous_key_release (def)
#   L08287:   MisoraApp._sync_continuous_box_from_widget (def)
#   L08291:   MisoraApp._highlight_dialogue_matches (def)
#   L08325:   MisoraApp._highlight_continuous_matches (def)
#   L08353:   MisoraApp._commit_speaker_edit (def)
#   L08422:   MisoraApp._on_speaker_edited (def)
#   L08426:   MisoraApp._refresh_continuous_box_header (def)
#   L08441:   MisoraApp._on_dialogue_key_up (def)
#   L08451:   MisoraApp._on_dialogue_key_down (def)
#   L08461:   MisoraApp._commit_widget_edit (def)
#   L08559:   MisoraApp._on_dialogue_edited (def)
#   L08645:   MisoraApp._update_box0_char_counter (def)
#   L08655:   MisoraApp._on_box0_metadata_edited (def)
#   L08693:   MisoraApp.on_prev_box (def)
#   L08713:   MisoraApp.on_next_box (def)
#   L08730:   MisoraApp.is_box_locked (def)
#   L08738:   MisoraApp.on_toggle_lock_current_box (def)
#   L08774:   MisoraApp._resync_box_indices_from_uids (def)
#   L08788:   MisoraApp._update_rendered_char_count (def)
#   L08807:   MisoraApp.on_revert_box (def)
#   L08811:   MisoraApp.on_insert_playername (def)
#   L08817:   MisoraApp.on_save (def)
#   L08968:   MisoraApp._save_active_document_state (def)
#   L09004:   MisoraApp._save_document_entry (def)
#   L09089:   MisoraApp.on_reload (def)
#   L09096:   MisoraApp.on_start_search (def)
#   L09230:   MisoraApp._reset_search_results_state (def)
#   L09242:   MisoraApp.on_cancel_search (def)
#   L09249:   MisoraApp._run_background_search (def)
#   L09300:   MisoraApp._process_search_queue (def)
# ======================================================================

    def _render_continuous_view(self) -> None:
        """Render all dialogue boxes sequentially as a Box Card Stream."""
        compiled = self.var_preview_compiled.get()
        self._suppress_continuous_events = True
        t = self.theme
        d_fam = self.var_font_family.get() if hasattr(self, "var_font_family") else "Segoe UI"
        d_sz = int(self.prefs.get("dialogue_font_size", 12))

        try:
            self._card_widgets.clear()
            # If plain text file: keep legacy txt_continuous view
            if not self.is_bundle_file and not self.current_doc:
                if hasattr(self, "cont_canvas") and self._is_widget_packed(self.cont_canvas):
                    self.cont_canvas.pack_forget()
                    self.cont_scroll_y.pack_forget()
                if hasattr(self, "txt_continuous") and not self._is_widget_packed(self.txt_continuous):
                    self.txt_continuous.pack(side="left", fill="both", expand=True)
                self.txt_continuous.config(state="normal")
                self.txt_continuous.delete("1.0", tk.END)
                if compiled:
                    self._insert_compiled_ngui_text(self.txt_continuous, "1.0", self._plain_text_content)
                    self.txt_continuous.config(state="disabled")
                else:
                    self.txt_continuous.insert("1.0", self._plain_text_content)
                    self._highlight_ngui_tags_for_widget(self.txt_continuous)
                return

            # Multi-Box Story Documents: Box Card Stream
            if hasattr(self, "txt_continuous") and self._is_widget_packed(self.txt_continuous):
                self.txt_continuous.pack_forget()
            if hasattr(self, "gutter_cont") and self._is_widget_packed(self.gutter_cont):
                self.gutter_cont.pack_forget()

            if hasattr(self, "cont_scroll_y") and not self._is_widget_packed(self.cont_scroll_y):
                self.cont_scroll_y.pack(side="right", fill="y")
            if hasattr(self, "cont_canvas") and not self._is_widget_packed(self.cont_canvas):
                self.cont_canvas.pack(side="left", fill="both", expand=True)

            # Clear existing cards
            if hasattr(self, "cont_stream_frame"):
                for child in self.cont_stream_frame.winfo_children():
                    child.destroy()

            if not self.current_doc or not self.current_doc.boxes:
                return

            gutter_bg = "#e8e8e8" if self._is_light_theme() else "#2d2d30"
            gutter_fg = "#707070" if self._is_light_theme() else "#858585"

            # 1. Card #0: Story Metadata Card
            if self.current_doc.has_metadata():
                meta = self.current_doc.get_metadata()
                is_active_0 = getattr(self, "is_box0_active", False)
                box0_bg = t["highlight_bg"] if is_active_0 else ("#dfd1f5" if self._is_light_theme() else "#2d1d29")
                box0_border = "#bca0e8" if self._is_light_theme() else "#4a3556"
                card_0 = tk.Frame(self.cont_stream_frame, bg=box0_bg, highlightbackground=box0_border, highlightthickness=1)
                hdr_0 = tk.Frame(card_0, bg=box0_bg, padx=4, pady=1)
                lbl_badge_0 = tk.Label(hdr_0, text="◆ [BOX #000]", font=("Consolas", max(8, d_sz - 3), "bold"), fg=t["misora_pink"], bg=box0_bg)
                lbl_badge_0.pack(side="left")
                lbl_title_0 = tk.Label(hdr_0, text="[STORY METADATA & SYNOPSIS]", font=(d_fam, max(8, d_sz - 3), "bold"), fg=t["fg_text"], bg=box0_bg)
                lbl_title_0.pack(side="left", padx=(6, 4))
                hdr_0.pack(fill="x")

                meta_body = tk.Frame(card_0, bg=box0_bg, padx=4, pady=1)
                tk.Label(meta_body, text=f"Title: {meta.get('title', '')}   |   Subtitle: {meta.get('subtitle', '')}", font=(d_fam, max(7, d_sz - 3)), fg=t["fg_muted"], bg=box0_bg).pack(anchor="w")
                summary_lines = max(2, min(8, meta.get("summary", "").count("\n") + 1))
                txt_summary = tk.Text(
                    meta_body,
                    wrap="word",
                    undo=False,
                    height=summary_lines,
                    font=(d_fam, d_sz),
                    bg=t["bg_editor"],
                    fg=t["fg_text"],
                    insertbackground=t["misora_pink"],
                    selectbackground=t["highlight_bg"],
                    selectforeground=t["misora_pink"],
                    bd=1,
                    relief="solid",
                    highlightthickness=0,
                    padx=8,
                    pady=3,
                    spacing1=2,
                    spacing3=2
                )
                txt_summary.insert("1.0", meta.get("summary", ""))
                txt_summary.pack(fill="x", pady=(1, 2))
                meta_body.pack(fill="x")

                # Bindings for Card #0
                self._install_shortcuts_bindtag(txt_summary)
                txt_summary.bind("<FocusIn>", lambda e: self._on_card_focus_in(-1))
                txt_summary.bind("<KeyRelease>", lambda e, w=txt_summary: self._commit_widget_edit(w))
                txt_summary.bind("<<Cut>>", lambda e, w=txt_summary: self.after_idle(lambda: self._commit_widget_edit(w)))
                txt_summary.bind("<<Paste>>", lambda e, w=txt_summary: self.after_idle(lambda: self._commit_widget_edit(w)))
                txt_summary.bind("<Control-a>", lambda e, w=txt_summary: (w.tag_add("sel", "1.0", "end-1c"), "break")[1])
                txt_summary.bind("<Control-A>", lambda e, w=txt_summary: (w.tag_add("sel", "1.0", "end-1c"), "break")[1])

                for w in (card_0, hdr_0, lbl_badge_0, lbl_title_0, meta_body, txt_summary):
                    w.bind("<MouseWheel>", self._on_cont_mousewheel)

                card_0.pack(fill="x", padx=6, pady=(1, 2))

                self._card_widgets[-1] = {
                    "card": card_0,
                    "hdr": hdr_0,
                    "txt": txt_summary,
                    "lbl_badge": lbl_badge_0,
                    "lbl_title": lbl_title_0,
                }

            # 2. Cards #1..N: Dialogue Box Cards
            for i, box in enumerate(self.current_doc.boxes):
                is_active = (not getattr(self, "is_box0_active", False) and i == self.current_box_idx)
                hdr_bg = t["highlight_bg"] if is_active else t["bg_panel"]
                card_frame = tk.Frame(self.cont_stream_frame, bg=t["bg_panel"])
                hdr = tk.Frame(card_frame, bg=hdr_bg, padx=4, pady=0)

                # Select Box Checkbox (when Select Box Mode is active)
                if self.var_select_box_mode.get():
                    var_box_sel = tk.BooleanVar(master=self, value=(i in self._selected_boxes))
                    def _make_box_sel_cmd(b_idx, v):
                        def _cmd():
                            if v.get():
                                self._selected_boxes.add(b_idx)
                            else:
                                self._selected_boxes.discard(b_idx)
                        return _cmd
                    cb_sel = tk.Checkbutton(
                        hdr,
                        variable=var_box_sel,
                        command=_make_box_sel_cmd(i, var_box_sel),
                        bg=hdr_bg,
                        activebackground=hdr_bg,
                        selectcolor=t["bg_panel"],
                        bd=0,
                        cursor="hand2",
                    )
                    cb_sel.pack(side="left", padx=(0, 2))
                    cb_sel.bind("<MouseWheel>", self._on_cont_mousewheel)

                lbl_badge = tk.Label(hdr, text=f"◆ [BOX #{i+1:03d}]", font=("Consolas", max(8, d_sz - 3), "bold"), fg=t["misora_pink"], bg=hdr_bg)
                lbl_badge.pack(side="left")

                sp_text = box.speaker if box.speaker else "(Narration)"
                sp_fg = t["fg_text"] if box.speaker else t["fg_muted"]
                sp_font = (d_fam, max(8, d_sz - 3), "bold" if box.speaker else "italic")
                lbl_sp = tk.Label(hdr, text=sp_text, font=sp_font, fg=sp_fg, bg=hdr_bg)
                lbl_sp.pack(side="left", padx=(6, 4))

                vc_text = f"♪ {box.voice_cue}" if box.voice_cue else ""
                lbl_vc = tk.Label(hdr, text=vc_text, font=("Segoe UI", max(7, d_sz - 4)), fg=t["accent_blue"], bg=hdr_bg)
                lbl_vc.pack(side="left", padx=(2, 4))

                # Translation Lock indicator (Rule 20 D8)
                is_locked = i in getattr(self, "_locked_boxes", set())
                lbl_lock = tk.Label(hdr, text="🔒" if is_locked else "", font=("Segoe UI", max(7, d_sz - 4)), fg=t["accent_yellow"], bg=hdr_bg)
                lbl_lock.pack(side="left", padx=(2, 4))

                if len(box.segs) > 1:
                    lbl_segs = tk.Label(hdr, text=f"{len(box.segs)} segs", font=("Segoe UI", max(7, d_sz - 4), "bold"), fg=t["misora_pink"], bg=hdr_bg)
                    lbl_segs.pack(side="left", padx=(2, 4))

                # Rendered character count (Rule 19 / GAME-BOX-PREVIEW)
                char_len = get_rendered_length(box.clean_text)
                lbl_chars = tk.Label(hdr, text=f"({char_len} chars)", font=("Segoe UI", max(7, d_sz - 4)), fg=t["fg_muted"], bg=hdr_bg)
                lbl_chars.pack(side="right", padx=(4, 6))

                hdr.pack(fill="x", pady=0)

                # Editor Row with dynamic line-number gutter
                editor_row = tk.Frame(card_frame, bg=t["bg_panel"])
                editor_row.pack(fill="x", padx=0, pady=0)

                line_count = max(1, box.clean_text.count("\n") + 1)
                eff_height = max(2, min(10, line_count))

                gutter = tk.Text(
                    editor_row,
                    width=2,
                    height=eff_height,
                    font=("Consolas", max(8, d_sz - 2)),
                    bg=gutter_bg,
                    fg=gutter_fg,
                    bd=0,
                    relief="flat",
                    wrap="none",
                    takefocus=0,
                    cursor="arrow",
                    padx=1,
                    pady=3,
                    spacing1=2,
                    spacing3=2,
                )
                gutter.insert("1.0", "\n".join(str(n) for n in range(1, line_count + 1)))
                gutter.config(state="disabled")
                if self.show_line_numbers:
                    gutter.pack(side="left", fill="y", padx=(0, 2))

                txt = tk.Text(
                    editor_row,
                    wrap="word",
                    undo=False,
                    height=eff_height,
                    font=(d_fam, d_sz),
                    bg=t["bg_editor"],
                    fg=t["fg_text"],
                    insertbackground=t["misora_pink"],
                    selectbackground=t["highlight_bg"],
                    selectforeground=t["misora_pink"],
                    bd=1,
                    relief="solid",
                    highlightthickness=0,
                    padx=8,
                    pady=3,
                    spacing1=2,
                    spacing3=2
                )
                self._configure_editor_rich_tags(txt, d_fam, d_sz)
                if compiled:
                    self._insert_compiled_ngui_text(txt, "1.0", box.clean_text)
                    txt.config(state="disabled")
                else:
                    txt.insert("1.0", box.clean_text)
                    self._highlight_ngui_tags_for_widget(txt)

                txt.pack(side="left", fill="x", expand=True)

                # Bindings on card widgets
                for w in (card_frame, hdr, lbl_badge, lbl_sp, lbl_vc, editor_row, gutter, txt):
                    w.bind("<MouseWheel>", self._on_cont_mousewheel)

                self._install_shortcuts_bindtag(txt)
                txt.bind("<KeyRelease>", lambda e, idx=i, w=txt, g=gutter: self._commit_widget_edit(w))
                txt.bind("<<Cut>>", lambda e, w=txt: self.after_idle(lambda: self._commit_widget_edit(w)))
                txt.bind("<FocusIn>", lambda e, idx=i: self._on_card_focus_in(idx))
                txt.bind("<Control-a>", lambda e, w=txt: (w.tag_add("sel", "1.0", "end-1c"), "break")[1])
                txt.bind("<Control-A>", lambda e, w=txt: (w.tag_add("sel", "1.0", "end-1c"), "break")[1])
                txt.bind("<Control-Shift-C>", lambda e: (self.on_copy_script(), "break")[1])
                txt.bind("<Control-Shift-c>", lambda e: (self.on_copy_script(), "break")[1])
                txt.bind("<Control-v>", lambda e, idx=i, w=txt: self._on_card_paste_caret(idx, w))
                txt.bind("<<Paste>>", lambda e, idx=i, w=txt: (self._on_card_paste_caret(idx, w) or self.after_idle(lambda: self._commit_widget_edit(w))))
                txt.bind("<Control-Shift-V>", lambda e: (self.on_paste_cross_box(), "break")[1])
                txt.bind("<Control-Shift-v>", lambda e: (self.on_paste_cross_box(), "break")[1])
                txt.bind("<Control-b>", lambda e, w=txt: (self._card_shortcut_wrap(w, "[b]", "[/b]"), "break")[1])
                txt.bind("<Control-i>", lambda e, w=txt: (self._card_shortcut_wrap(w, "[i]", "[/i]"), "break")[1])
                txt.bind("<Control-u>", lambda e, w=txt: (self._card_shortcut_wrap(w, "[u]", "[/u]"), "break")[1])

                card_frame.pack(fill="x", padx=6, pady=(1, 2))

                self._card_widgets[i] = {
                    "card": card_frame,
                    "hdr": hdr,
                    "editor_row": editor_row,
                    "gutter": gutter,
                    "txt": txt,
                    "lbl_badge": lbl_badge,
                    "lbl_sp": lbl_sp,
                    "lbl_vc": lbl_vc,
                }

            self._highlight_continuous_matches()
        finally:
            self._suppress_continuous_events = False

    def _focus_continuous_box(
        self,
        box_idx: int,
        move_cursor: bool = True,
        char_offset: int = 0,
        explicit_span: Optional[Tuple[int, int]] = None
    ) -> None:
        """Scroll Continuous View to `box_idx`, highlight its card header, and sync metadata."""
        if not self.current_doc:
            return

        total = len(self.current_doc.boxes) if self.current_doc.boxes else 0
        if box_idx == -1:
            self.is_box0_active = True
            target_idx = -1
        else:
            self.is_box0_active = False
            self.current_box_idx = max(0, min(box_idx, total - 1)) if total > 0 else 0
            target_idx = self.current_box_idx

        self._highlight_active_card_header(target_idx)
        self._sync_header_controls_for_card(target_idx)
        self._update_raw_view()

        if hasattr(self, "_card_widgets") and target_idx in self._card_widgets:
            card_info = self._card_widgets[target_idx]
            card = card_info["card"]
            self.update_idletasks()
            try:
                total_h = self.cont_stream_frame.winfo_height()
                if total_h > 0:
                    card_y = card.winfo_y()
                    fraction = max(0.0, min(1.0, card_y / total_h))
                    self.cont_canvas.yview_moveto(fraction)
            except Exception:
                pass

            txt_w = card_info["txt"]
            if move_cursor and str(txt_w.cget("state")) != "disabled":
                try:
                    target_pos = f"1.0 + {max(0, char_offset)}c"
                    txt_w.mark_set("insert", target_pos)
                    txt_w.see("insert")
                    txt_w.focus_set()
                except Exception:
                    pass

            if explicit_span is not None and not self.var_preview_compiled.get():
                s, e = explicit_span
                if e > s:
                    txt_w.tag_remove("search_hit", "1.0", tk.END)
                    txt_w.tag_add("search_hit", f"1.0 + {s}c", f"1.0 + {e}c")
                    txt_w.see(f"1.0 + {s}c")

    def _find_continuous_box_at_index(self, tk_index: str) -> Optional[int]:
        """Return active box index (compatibility shim for Card Stream architecture)."""
        if getattr(self, "is_box0_active", False):
            return -1
        return self.current_box_idx

    def _nearest_continuous_box_to_index(self, tk_index: str) -> int:
        """Return active box index (compatibility shim for Card Stream architecture)."""
        return self.current_box_idx

    def _on_continuous_cursor_moved(self, event: Optional[tk.Event] = None) -> None:
        """Compatibility shim for Card Stream (handled via _on_card_focus_in)."""
        pass

    def _on_continuous_key_guard(self, event: tk.Event) -> Optional[str]:
        """Compatibility shim for Card Stream."""
        return None

    def _on_continuous_copy(self, _event: Optional[tk.Event] = None) -> Optional[str]:
        """Compatibility shim for Card Stream."""
        return None

    def _on_continuous_paste_guard(self, _event: tk.Event) -> Optional[str]:
        """Compatibility shim for Card Stream."""
        return None

    def _on_continuous_cut_guard(self, _event: tk.Event) -> Optional[str]:
        """Compatibility shim for Card Stream."""
        return None

    def _on_continuous_key_release(self, _event: tk.Event) -> None:
        """Compatibility shim for Card Stream."""
        self._flush_continuous_card_edits()

    def _sync_continuous_box_from_widget(self) -> None:
        """Persist card edits to StoryDocument or plain text."""
        self._flush_continuous_card_edits()

    def _highlight_dialogue_matches(self, explicit_span: Optional[Tuple[int, int]] = None) -> None:
        """Highlight active search keyword spans inside the single-box dialogue editor."""
        if self.var_preview_compiled.get():
            return

        self.txt_dialogue.tag_remove("search_hit", "1.0", tk.END)

        if explicit_span is not None:
            s, e = explicit_span
            if e > s:
                start_idx = f"1.0 + {s}c"
                end_idx = f"1.0 + {e}c"
                self.txt_dialogue.tag_add("search_hit", start_idx, end_idx)
                self.txt_dialogue.see(start_idx)
                return

        if not self.active_search_options or not self.active_search_options.query.strip():
            return

        text = self.txt_dialogue.get("1.0", "end-1c")
        if not text:
            return

        try:
            matcher = self.search_engine._compile_matcher(self.active_search_options)
            matches = matcher(text)
            for s, e, _ in matches:
                if e > s:
                    self.txt_dialogue.tag_add("search_hit", f"1.0 + {s}c", f"1.0 + {e}c")
            if matches:
                self.txt_dialogue.see(f"1.0 + {matches[0][0]}c")
        except Exception:
            pass

    def _highlight_continuous_matches(self) -> None:
        """Highlight active search keyword spans across all cards in Continuous View."""
        if self.var_preview_compiled.get():
            return
        if not hasattr(self, "_card_widgets") or not self._card_widgets:
            return

        matcher = None
        if self.active_search_options and self.active_search_options.query.strip():
            try:
                matcher = self.search_engine._compile_matcher(self.active_search_options)
            except Exception:
                matcher = None

        for b_idx, card_info in self._card_widgets.items():
            txt_w = card_info.get("txt")
            if not txt_w:
                continue
            try:
                txt_w.tag_remove("search_hit", "1.0", tk.END)
                if matcher:
                    box_tx = txt_w.get("1.0", "end-1c")
                    for s, e, _ in matcher(box_tx):
                        if e > s:
                            txt_w.tag_add("search_hit", f"1.0 + {s}c", f"1.0 + {e}c")
            except Exception:
                pass

    def _commit_speaker_edit(self) -> bool:
        """Central edit commit path for speaker entry edits (Rule 11, F20).
        Returns True if a mutation occurred, False if no-op or aborted.
        """
        if getattr(self, "_suppress_continuous_events", False):
            return False
        if getattr(self, "is_box0_active", False):
            return False
        if not self.current_doc or not self.current_doc.boxes:
            return False
        if not (0 <= self.current_box_idx < len(self.current_doc.boxes)):
            return False

        idx = self.current_box_idx
        box = self.current_doc.boxes[idx]
        old_sp = box.speaker
        new_sp = self.speaker_var.get()

        # Resolve current text cleanly from active view
        if getattr(self, "var_continuous_view", None) and self.var_continuous_view.get():
            if hasattr(self, "_card_widgets") and idx in self._card_widgets:
                cur_tx = self._card_widgets[idx]["txt"].get("1.0", "end-1c")
            else:
                cur_tx = box.clean_text
        else:
            if getattr(self, "var_preview_compiled", None) and self.var_preview_compiled.get():
                cur_tx = box.clean_text
            elif hasattr(self, "txt_dialogue") and self.txt_dialogue.winfo_exists():
                cur_tx = self.txt_dialogue.get("1.0", "end-1c")
            else:
                cur_tx = box.clean_text

        if old_sp == new_sp:
            return False

        self.undo_journal.record(
            BoxEditDelta(
                box_index=idx,
                old_speaker=old_sp,
                new_speaker=new_sp,
                old_text=box.clean_text,
                new_text=cur_tx,
                file_path=str(self.current_file_path or ""),
                box_uid=box.uid,
                source="keyboard",
            ),
            label=f"Rename speaker #{idx + 1}"
        )

        try:
            self.current_doc.inject_box(idx, new_sp, cur_tx)
        except Exception as ex:
            self.logger.error("AST", f"Failed to inject speaker rename: {ex}")
            return False

        self._modified_boxes.add(idx)
        self._mark_document_dirty(self.current_file_path)

        if hasattr(self, "_refresh_continuous_box_header"):
            self._refresh_continuous_box_header(idx)
        elif hasattr(self, "_card_widgets") and idx in self._card_widgets:
            lbl_sp = self._card_widgets[idx].get("lbl_sp")
            if lbl_sp and lbl_sp.winfo_exists():
                lbl_sp.config(text=new_sp if new_sp else "(Narration)")

        self._update_raw_view()
        self._dirty_state_changed()
        return True

    def _on_speaker_edited(self) -> None:
        """Triggered when editing the pinned Speaker entry in either Page or Continuous mode."""
        self._commit_speaker_edit()

    def _refresh_continuous_box_header(self, box_idx: int) -> None:
        """Update a single box header in Continuous View in-place when its speaker changes."""
        if not self.current_doc or not (0 <= box_idx < len(self.current_doc.boxes)):
            return
        if not hasattr(self, "_card_widgets") or box_idx not in self._card_widgets:
            return
        box = self.current_doc.boxes[box_idx]
        card_info = self._card_widgets[box_idx]
        lbl_sp = card_info.get("lbl_sp")
        if lbl_sp:
            t = self.theme
            speaker_disp = box.speaker if box.speaker else "(Narration)"
            speaker_color = t["misora_pink"] if box.speaker else t["fg_muted"]
            lbl_sp.config(text=speaker_disp, fg=speaker_color)

    def _on_dialogue_key_up(self, _event: tk.Event) -> Optional[str]:
        """Navigate to previous box when pressing Up at top line of Clean Dialogue View."""
        if self.txt_dialogue.compare("insert linestart", "==", "1.0"):
            if self.current_box_idx > 0:
                self.on_prev_box()
                self.txt_dialogue.mark_set("insert", "end-1c")
                self.txt_dialogue.see("insert")
                return "break"
        return None

    def _on_dialogue_key_down(self, _event: tk.Event) -> Optional[str]:
        """Navigate to next box when pressing Down at bottom line of Clean Dialogue View."""
        if self.txt_dialogue.compare("insert lineend", ">=", "end-1c"):
            if self.current_doc and self.current_box_idx < len(self.current_doc.boxes) - 1:
                self.on_next_box()
                self.txt_dialogue.mark_set("insert", "1.0")
                self.txt_dialogue.see("insert")
                return "break"
        return None

    def _commit_widget_edit(self, widget: Optional[tk.Widget] = None) -> None:
        """Central edit commit path for all widget edits, ribbon wrappers, cut/paste, and metadata (Rule 11)."""
        if getattr(self, "_suppress_continuous_events", False):
            return
        if getattr(self, "var_preview_compiled", None) and self.var_preview_compiled.get():
            return

        if widget is None:
            widget = self._get_active_text_widget()
        if widget is None:
            return

        # 1. Continuous View Box 0 Metadata Card (-1)
        if (
            self.current_doc
            and self.current_doc.has_metadata()
            and -1 in getattr(self, "_card_widgets", {})
            and widget == self._card_widgets[-1].get("txt")
        ):
            new_sum = widget.get("1.0", "end-1c")
            meta = self.current_doc.get_metadata()
            old_sum = meta.get("summary", "")
            if old_sum != new_sum:
                self.undo_journal.record(
                    MetadataDelta(
                        file_path=str(self.current_file_path or ""),
                        old_title=meta.get("title", ""),
                        new_title=meta.get("title", ""),
                        old_subtitle=meta.get("subtitle", ""),
                        new_subtitle=meta.get("subtitle", ""),
                        old_summary=old_sum,
                        new_summary=new_sum,
                    ),
                    label="Edit Synopsis"
                )
                self.current_doc.set_metadata(summary=new_sum)
                self._mark_document_dirty(self.current_file_path)
                if hasattr(self, "txt_box0_summary") and self.txt_box0_summary.winfo_exists():
                    self.txt_box0_summary.delete("1.0", tk.END)
                    self.txt_box0_summary.insert("1.0", new_sum)
                self._update_raw_view()
                self._dirty_state_changed()
            return

        # 2. Page View Box 0 Metadata Widgets
        is_box0 = (
            getattr(self, "is_box0_active", False)
            or widget in (
                getattr(self, "txt_box0_summary", None),
                getattr(self, "entry_box0_title", None),
                getattr(self, "entry_box0_subtitle", None),
            )
        )
        if is_box0:
            if self._on_box0_metadata_edited():
                self._dirty_state_changed()
            self._update_box0_char_counter()
            return

        # 2. Speaker Entry
        if widget == getattr(self, "entry_speaker", None):
            self._commit_speaker_edit()
            return

        # 3. Page View Dialogue Editor (txt_dialogue)
        if widget == getattr(self, "txt_dialogue", None):
            if self._on_dialogue_edited():
                self._dirty_state_changed()
            return

        # 4. Continuous View Card text widgets
        if hasattr(self, "_card_widgets") and self._card_widgets:
            for b_idx, card_dict in list(self._card_widgets.items()):
                if card_dict.get("txt") == widget and b_idx >= 0:
                    gutter = card_dict.get("gutter")
                    if self._on_card_text_edited(b_idx, widget, gutter):
                        self._dirty_state_changed()
                    return

        # 5. Continuous View plain text fallback
        if widget == getattr(self, "txt_continuous", None):
            new_tx = widget.get("1.0", "end-1c")
            if new_tx != getattr(self, "_plain_text_content", ""):
                self.undo_journal.record(
                    PlainTextDelta(
                        file_path=str(self.current_file_path or ""),
                        old_content=self._plain_text_content,
                        new_content=new_tx,
                    ),
                    label=f"Edit {self.current_file_path.name if self.current_file_path else 'text'}"
                )
                self._plain_text_content = new_tx
                if self.current_file_path and self.current_file_path in self.open_documents:
                    self.open_documents[self.current_file_path]["plain_text"] = new_tx
                self._mark_document_dirty(self.current_file_path)
                self._dirty_state_changed()
            return

    def _on_dialogue_edited(self) -> bool:
        """Triggered on every keystroke in the single-box Game Display dialogue editor.

        Returns True if a real mutation occurred (content changed), False if no-op (S2).
        Only marks dirty and records undo when content actually changed.
        """
        if self.var_preview_compiled.get():
            return False

        if self.current_doc and self.current_doc.boxes:
            idx = self.current_box_idx
            box = self.current_doc.boxes[idx]
            old_sp = box.speaker
            old_tx = box.clean_text
            new_tx = self.txt_dialogue.get("1.0", "end-1c")
            # S2: guard no-op — dirty/undo only on actual change
            if old_tx == new_tx:
                self._auto_resize_dialogue_box()
                self._highlight_ngui_tags()
                self._highlight_dialogue_matches()
                return False
            box_uid = box.segs[0].record.uid if box.segs else None
            old_segs = [s.text for s in box.segs] if len(box.segs) > 1 else None
            try:
                self.current_doc.inject_box(idx, None, new_tx)
            except Exception as e:
                self.logger.exception(f"Failed to inject box {idx}:", e)
                self.set_status(f"Error updating box #{idx + 1}: {e}", is_error=True)
                return False

            new_segs = None
            if old_segs is not None:
                refreshed_box = next((b for b in self.current_doc.boxes if b.segs and b.segs[0].record.uid == box_uid), None)
                if refreshed_box:
                    new_segs = [s.text for s in refreshed_box.segs]

            delta = BoxEditDelta(
                box_index=idx,
                old_speaker=old_sp,
                new_speaker=old_sp,
                old_text=old_tx,
                new_text=new_tx,
                file_path=str(self.current_file_path or ""),
                box_uid=box_uid,
                source=getattr(self, "_current_edit_source", "keyboard"),
                old_seg_texts=old_segs,
                new_seg_texts=new_segs,
            )
            self.undo_journal.record(delta, label=f"Edit box #{idx + 1}")
            self._modified_boxes.add(idx)
            self._mark_document_dirty(self.current_file_path)
            try:
                self._update_raw_view()
            except Exception:
                pass
            self._auto_resize_dialogue_box()
            self._highlight_ngui_tags()
            self._highlight_dialogue_matches()
            self._update_rendered_char_count(new_tx)
            self._update_gutter_clean()
            return True
        else:
            old_content = self._plain_text_content
            new_content = self.txt_dialogue.get("1.0", "end-1c")
            # S2: guard no-op
            if old_content == new_content:
                self._auto_resize_dialogue_box()
                return False
            self.undo_journal.record(
                PlainTextDelta(
                    file_path=str(self.current_file_path or ""),
                    old_content=old_content,
                    new_content=new_content,
                ),
                label=f"Edit {self.current_file_path.name if self.current_file_path else 'text'}"
            )
            self._plain_text_content = new_content
            if self.current_file_path and self.current_file_path in self.open_documents:
                self.open_documents[self.current_file_path]["plain_text"] = new_content
            self._mark_document_dirty(self.current_file_path)
            self._auto_resize_dialogue_box()
            self._highlight_ngui_tags()
            self._highlight_dialogue_matches()
            self._update_gutter_clean()
            return True

    def _update_box0_char_counter(self) -> None:
        if not hasattr(self, "lbl_box0_summary_len") or not hasattr(self, "txt_box0_summary"):
            return
        txt = self.txt_box0_summary.get("1.0", "end-1c")
        chars = len(txt)
        lines = txt.count("\n") + (1 if txt else 0)
        self.lbl_box0_summary_len.config(
            text=f"Summary: {chars} chars | {lines} lines (In-game display: ~3-4 lines)"
        )

    def _on_box0_metadata_edited(self) -> bool:
        """Triggered on keystroke when editing Episode Title, Subtitle, or Synopsis in Box 0. Returns True if mutated (BUG-30)."""
        if not self.current_doc or not self.current_doc.has_metadata():
            return False
        meta = self.current_doc.get_metadata()
        old_title = meta.get("title", "")
        old_subtitle = meta.get("subtitle", "")
        old_summary = meta.get("summary", "")

        new_title = self.var_box0_title.get()
        new_subtitle = self.var_box0_subtitle.get()
        new_summary = self.txt_box0_summary.get("1.0", "end-1c")

        if (old_title, old_subtitle, old_summary) != (new_title, new_subtitle, new_summary):
            self.undo_journal.record(
                MetadataDelta(
                    file_path=str(self.current_file_path or ""),
                    old_title=old_title,
                    new_title=new_title,
                    old_subtitle=old_subtitle,
                    new_subtitle=new_subtitle,
                    old_summary=old_summary,
                    new_summary=new_summary,
                ),
                label="Edit story metadata (Box 0)"
            )
            self.current_doc.set_metadata(title=new_title, subtitle=new_subtitle, summary=new_summary)
            self._mark_document_dirty(self.current_file_path)
            if hasattr(self, "_card_widgets") and -1 in self._card_widgets:
                c0_txt = self._card_widgets[-1].get("txt")
                if c0_txt and c0_txt.winfo_exists():
                    c0_txt.delete("1.0", tk.END)
                    c0_txt.insert("1.0", new_summary)
            self._update_box0_char_counter()
            self._update_raw_view()
            return True
        return False

    def on_prev_box(self) -> None:
        if self.is_box0_active:
            return

        if self.current_doc and self.current_box_idx == 0:
            if self.current_doc.has_metadata():
                self.is_box0_active = True
                if self.var_continuous_view.get():
                    self._focus_continuous_box(-1, move_cursor=True)
                else:
                    self._update_views()
            return

        if self.current_doc and self.current_box_idx > 0:
            self.current_box_idx -= 1
            if self.var_continuous_view.get():
                self._focus_continuous_box(self.current_box_idx, move_cursor=True)
            else:
                self._update_views()

    def on_next_box(self) -> None:
        if self.is_box0_active:
            self.is_box0_active = False
            self.current_box_idx = 0
            if self.var_continuous_view.get():
                self._focus_continuous_box(0, move_cursor=True)
            else:
                self._update_views()
            return

        if self.current_doc and self.current_box_idx < len(self.current_doc.boxes) - 1:
            self.current_box_idx += 1
            if self.var_continuous_view.get():
                self._focus_continuous_box(self.current_box_idx, move_cursor=True)
            else:
                self._update_views()

    def is_box_locked(self, box_idx: int) -> bool:
        """Check if dialogue box at box_idx is locked against translation / batch mutations (Rule 20 D8 / S06)."""
        if self.current_doc and 0 <= box_idx < len(self.current_doc.boxes):
            b_uid = _get_box_uid(self.current_doc.boxes[box_idx])
            if b_uid is not None and b_uid in getattr(self, "_locked_box_uids", set()):
                return True
        return box_idx in getattr(self, "_locked_boxes", set())

    def on_toggle_lock_current_box(self) -> None:
        """Toggle Translation Lock on active dialogue box (Ctrl+L / Rule 20 D8 / S06)."""
        if not self.current_doc or not self.current_doc.boxes:
            return
        if getattr(self, "is_box0_active", False):
            self.show_toast("Box 0 metadata cannot be locked.")
            return
        b_idx = self.current_box_idx
        if not (0 <= b_idx < len(self.current_doc.boxes)):
            return
        box = self.current_doc.boxes[b_idx]
        b_uid = _get_box_uid(box)

        if not hasattr(self, "_locked_box_uids"):
            self._locked_box_uids = set()
        if not hasattr(self, "_locked_boxes"):
            self._locked_boxes = set()

        is_currently_locked = (b_uid is not None and b_uid in self._locked_box_uids) or (b_idx in self._locked_boxes)
        if is_currently_locked:
            if b_uid is not None:
                self._locked_box_uids.discard(b_uid)
            self._locked_boxes.discard(b_idx)
            self.show_toast(f"🔓 Box {b_idx + 1} unlocked")
        else:
            if b_uid is not None:
                self._locked_box_uids.add(b_uid)
            self._locked_boxes.add(b_idx)
            self.show_toast(f"🔒 Box {b_idx + 1} locked from batch/paste edits")

        if self.current_file_path:
            cur_p = Path(self.current_file_path).resolve()
            if cur_p in self.open_documents:
                self.open_documents[cur_p]["locked_box_uids"] = set(self._locked_box_uids)
        self._update_views()

    def _resync_box_indices_from_uids(self) -> None:
        """Re-sync positional indices (_locked_boxes, _modified_boxes, _original_box_texts) from authoritative UIDs (S06 / S07)."""
        if self.current_doc and self.current_doc.boxes:
            if hasattr(self, "_locked_box_uids"):
                self._locked_boxes = {i for i, b in enumerate(self.current_doc.boxes) if _get_box_uid(b) in self._locked_box_uids}
            if hasattr(self, "_modified_box_uids"):
                self._modified_boxes = {i for i, b in enumerate(self.current_doc.boxes) if _get_box_uid(b) in self._modified_box_uids}
            if hasattr(self, "_original_jp_by_uid"):
                self._original_box_texts = {i: self._original_jp_by_uid.get(_get_box_uid(b), b.clean_text) for i, b in enumerate(self.current_doc.boxes)}
        else:
            self._locked_boxes = set()
            self._modified_boxes = set()
            self._original_box_texts = {}

    def _update_rendered_char_count(self, text: str) -> None:
        """Update live rendered character counter and warn if text overflows dialogue frame (Rule 19 / GAME-BOX-PREVIEW)."""
        if not hasattr(self, "lbl_char_count") or not self.lbl_char_count.winfo_exists():
            return
        t = self.theme
        lines_info = measure_line_lengths(text)
        total_len = sum(l[1] for l in lines_info)
        max_line = max((l[1] for l in lines_info), default=0)
        if max_line > 45:
            self.lbl_char_count.config(
                text=f"Chars: {total_len} (Max: {max_line}) ⚠ Overflow",
                fg=t["misora_pink"]
            )
        else:
            self.lbl_char_count.config(
                text=f"Chars: {total_len} (Max: {max_line})",
                fg=t["fg_muted"]
            )

    def on_revert_box(self) -> None:
        if self.current_file_path:
            self.open_file(self.current_file_path, reload_from_disk=True)

    def on_insert_playername(self) -> None:
        self.apply_ngui_wrapper("{playername}", "")

    # -------------------------------------------------------------------------
    # Save & Patch Actions (Byte-Exact In-Place Repack)
    # -------------------------------------------------------------------------
    def on_save(self) -> bool:
        """Repack and save the active file in-place, with optional XUAT dictionary sync.

        Returns True on successful primary save, False on failure or no active file (S2).
        Secondary XUAT failure logs a warning, retains _modified_boxes, and returns True.
        """
        if not self.current_file_path:
            messagebox.showinfo("Nothing to Save", "No active file is open.")
            return False

        try:
            backup_dir = self._get_backup_dir()
            cur_p = Path(self.current_file_path).resolve()

            if not self.is_bundle_file and not self.current_doc:
                if self.current_file_path.is_file() and backup_dir:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    bak_path = backup_dir / f"{self.current_file_path.stem}.bak_{ts}{self.current_file_path.suffix}"
                    shutil.copy2(self.current_file_path, bak_path)
                if not getattr(self, "var_preview_compiled", None) or not self.var_preview_compiled.get():
                    content = self.txt_continuous.get("1.0", "end-1c") if self.var_continuous_view.get() else self.txt_dialogue.get("1.0", "end-1c")
                    self._plain_text_content = content
                else:
                    content = self._plain_text_content
                doc_entry = self.open_documents.get(cur_p, {})
                enc = doc_entry.get("encoding", "utf-8")
                has_bom = bool(doc_entry.get("has_bom", False))
                nl = doc_entry.get("newline", None)
                write_atomic_encoded(self.current_file_path, content, encoding=enc, has_bom=has_bom, newline=nl)
                if cur_p in self.open_documents:
                    self.open_documents[cur_p]["dirty"] = False
                    self.open_documents[cur_p]["plain_text"] = content
                self.is_dirty = False
                self._record_saved_checkpoint(self.current_file_path, None, content)
                self.undo_journal.mark_saved(str(self.current_file_path))
                self._dirty_state_changed()
                self.lbl_status.config(text=f"[SAVED] {self.current_file_path.name} saved successfully!")
                self.logger.info("File I/O", f"Saved plain text file '{self.current_file_path}' (backup in {backup_dir.name if backup_dir else 'none'})")
                return True

            if getattr(self, "is_box0_active", False):
                self._on_box0_metadata_edited()
            elif not self.current_doc.boxes:
                # 0-box metadata-only story (BUG-19)
                pass
            elif self.var_preview_compiled.get():
                if 0 <= self.current_box_idx < len(self.current_doc.boxes):
                    new_sp = self.speaker_var.get()
                    cur_tx = self.current_doc.boxes[self.current_box_idx].clean_text
                    self.current_doc.inject_box(self.current_box_idx, new_sp, cur_tx)
            elif self.var_continuous_view.get():
                self._sync_continuous_box_from_widget()
                if 0 <= self.current_box_idx < len(self.current_doc.boxes):
                    new_sp = self.speaker_var.get()
                    cur_tx = self.current_doc.boxes[self.current_box_idx].clean_text
                    self.current_doc.inject_box(self.current_box_idx, new_sp, cur_tx)
            else:
                if 0 <= self.current_box_idx < len(self.current_doc.boxes):
                    new_sp = self.speaker_var.get()
                    new_tx = self.txt_dialogue.get("1.0", "end-1c")
                    self.current_doc.inject_box(self.current_box_idx, new_sp, new_tx)
                    self._modified_boxes.add(self.current_box_idx)
                    box = self.current_doc.boxes[self.current_box_idx]
                    b_uid = _get_box_uid(box)
                    if b_uid is not None:
                        if not hasattr(self, "_modified_box_uids"):
                            self._modified_box_uids = set()
                        self._modified_box_uids.add(b_uid)

            if self.is_bundle_file:
                written_size = save_bundle_story(
                    self.current_unity_env,
                    self.current_text_obj,
                    self.current_doc,
                    self.current_file_path,
                    backup_dir=backup_dir
                )
                if cur_p in self.open_documents:
                    self.open_documents[cur_p]["dirty"] = False
                self.is_dirty = False
                self._record_saved_checkpoint(self.current_file_path, self.current_doc, "")
                self.undo_journal.mark_saved(str(self.current_file_path))
                self._dirty_state_changed()
                self.lbl_status.config(text=f"[SAVED & PATCHED] {self.current_file_path.name} ({written_size / 1024:.1f} KB) in-place successfully!")
                self.logger.info("File I/O", f"Patched bundle '{self.current_file_path}' ({written_size} bytes)")
            else:
                if self.current_file_path.is_file() and backup_dir:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    bak_path = backup_dir / f"{self.current_file_path.stem}.bak_{ts}{self.current_file_path.suffix}"
                    shutil.copy2(self.current_file_path, bak_path)
                v2_text = self.current_doc.to_v2_text()
                doc_entry = self.open_documents.get(cur_p, {})
                enc = doc_entry.get("encoding", "utf-8")
                has_bom = bool(doc_entry.get("has_bom", False))
                nl = doc_entry.get("newline", None)
                write_atomic_utf8(self.current_file_path, v2_text, encoding=enc, has_bom=has_bom, newline=nl)
                if cur_p in self.open_documents:
                    self.open_documents[cur_p]["dirty"] = False
                self.is_dirty = False
                self._record_saved_checkpoint(self.current_file_path, self.current_doc, "")
                self.undo_journal.mark_saved(str(self.current_file_path))
                self._dirty_state_changed()
                self.lbl_status.config(text=f"[SAVED] {self.current_file_path.name} saved successfully!")
                self.logger.info("File I/O", f"Saved v2 script '{self.current_file_path}'")

            if self.var_sync_xuat.get() and self.xuat_search_roots:
                try:
                    boxes_to_sync = sorted(self._modified_boxes) if self._modified_boxes else [self.current_box_idx]
                    synced_files: Set[str] = set()
                    for b_idx in boxes_to_sync:
                        if not (0 <= b_idx < len(self.current_doc.boxes)):
                            continue
                        box_obj = self.current_doc.boxes[b_idx]
                        orig_key = self._original_box_texts.get(b_idx, box_obj.clean_text)
                        matches = self.sync_manager.find_and_update(
                            japanese_key=orig_key,
                            new_english_text=box_obj.clean_text,
                            search_roots=self.xuat_search_roots,
                            backup=True,
                            backup_dir=backup_dir
                        )
                        for m in matches:
                            synced_files.add(m.file_path.name)
                        self._original_box_texts[b_idx] = box_obj.clean_text

                    if synced_files:
                        files_str = ", ".join(sorted(synced_files))
                        self.lbl_status.config(text=self.lbl_status.cget("text") + f" | Synced XUAT file(s): {files_str}")
                        self.logger.info("XUAT Sync", f"Synced XUAT file(s): {files_str}")
                    self._modified_boxes.clear()
                    if hasattr(self, "_modified_box_uids"):
                        self._modified_box_uids.clear()
                    if cur_p in self.open_documents:
                        self.open_documents[cur_p]["modified_box_uids"] = set()
                except Exception as xuat_err:
                    self.logger.warning("XUAT", f"Secondary XUAT sync failed (primary save succeeded): {xuat_err}")
                    self.lbl_status.config(text=self.lbl_status.cget("text") + f" | (XUAT sync failed: {xuat_err})")
            else:
                self._modified_boxes.clear()
                if hasattr(self, "_modified_box_uids"):
                    self._modified_box_uids.clear()
                if cur_p in self.open_documents:
                    self.open_documents[cur_p]["modified_box_uids"] = set()

            return True

        except Exception as e:
            self.logger.exception(f"Save/Patch failed for '{self.current_file_path}':", e)
            messagebox.showerror("Save Failed", f"Failed to repack or save:\n{e}")
            return False

    def _save_active_document_state(self) -> None:
        """Save mutable UI/view state for active document into open_documents cache (S06 / BUG-12)."""
        if not self.current_file_path:
            return
        cur_p = Path(self.current_file_path).resolve()
        if cur_p not in self.open_documents:
            return

        if not hasattr(self, "_modified_box_uids"):
            self._modified_box_uids = set()
        if not hasattr(self, "_locked_box_uids"):
            self._locked_box_uids = set()

        if self.current_doc and self.current_doc.boxes:
            for idx in getattr(self, "_modified_boxes", set()):
                if 0 <= idx < len(self.current_doc.boxes):
                    b_uid = _get_box_uid(self.current_doc.boxes[idx])
                    if b_uid is not None:
                        self._modified_box_uids.add(b_uid)
            for idx in getattr(self, "_locked_boxes", set()):
                if 0 <= idx < len(self.current_doc.boxes):
                    b_uid = _get_box_uid(self.current_doc.boxes[idx])
                    if b_uid is not None:
                        self._locked_box_uids.add(b_uid)

        entry = self.open_documents[cur_p]
        entry["current_box_idx"] = getattr(self, "current_box_idx", 0)
        entry["is_box0_active"] = getattr(self, "is_box0_active", False)
        entry["locked_box_uids"] = set(getattr(self, "_locked_box_uids", set()))
        entry["modified_box_uids"] = set(getattr(self, "_modified_box_uids", set()))
        if hasattr(self, "_original_jp_by_uid"):
            entry["original_jp_by_uid"] = dict(self._original_jp_by_uid)
        if not self.current_doc:
            entry["plain_text"] = getattr(self, "_plain_text_content", "")
        entry["dirty"] = getattr(self, "is_dirty", False)

    def _save_document_entry(self, path: Union[str, Path]) -> bool:
        """Save an open document entry to disk without switching active UI context (S06 / BUG-12)."""
        cur_p = Path(path).resolve()
        if cur_p == (Path(self.current_file_path).resolve() if self.current_file_path else None):
            return self.on_save()

        if cur_p not in self.open_documents:
            self.logger.warning("File I/O", f"Cannot save non-open document: {cur_p}")
            return False

        entry = self.open_documents[cur_p]
        backup_dir = self._get_backup_dir()
        modified_uids = set(entry.get("modified_box_uids", set()))

        try:
            if entry.get("is_bundle", False):
                env = entry.get("env")
                obj = entry.get("obj")
                doc = entry.get("doc")
                if not doc:
                    return False
                written_size = save_bundle_story(
                    env, obj, doc, cur_p, backup_dir=backup_dir
                )
                entry["dirty"] = False
                entry["modified_box_uids"] = set()
                self._record_saved_checkpoint(cur_p, doc, "")
                self.undo_journal.mark_saved(str(cur_p))
                self.logger.info("File I/O", f"Saved inactive bundle '{cur_p}' ({written_size} bytes)")
            elif entry.get("doc") is not None:
                doc = entry.get("doc")
                if cur_p.is_file() and backup_dir:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    bak_path = backup_dir / f"{cur_p.stem}.bak_{ts}{cur_p.suffix}"
                    shutil.copy2(cur_p, bak_path)
                v2_text = doc.to_v2_text()
                enc = entry.get("encoding", "utf-8")
                has_bom = bool(entry.get("has_bom", False))
                nl = entry.get("newline", None)
                write_atomic_encoded(cur_p, v2_text, encoding=enc, has_bom=has_bom, newline=nl)
                entry["dirty"] = False
                entry["modified_box_uids"] = set()
                self._record_saved_checkpoint(cur_p, doc, "")
                self.undo_journal.mark_saved(str(cur_p))
                self.logger.info("File I/O", f"Saved inactive v2 script '{cur_p}'")
            else:
                if cur_p.is_file() and backup_dir:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    bak_path = backup_dir / f"{cur_p.stem}.bak_{ts}{cur_p.suffix}"
                    shutil.copy2(cur_p, bak_path)
                content = entry.get("plain_text", "")
                enc = entry.get("encoding", "utf-8")
                has_bom = bool(entry.get("has_bom", False))
                nl = entry.get("newline", None)
                write_atomic_encoded(cur_p, content, encoding=enc, has_bom=has_bom, newline=nl)
                entry["dirty"] = False
                self._record_saved_checkpoint(cur_p, None, content)
                self.undo_journal.mark_saved(str(cur_p))
                self.logger.info("File I/O", f"Saved inactive plain text file '{cur_p}'")

            if self.var_sync_xuat.get() and self.xuat_search_roots and entry.get("doc") and modified_uids:
                doc = entry.get("doc")
                orig_by_uid = entry.get("original_jp_by_uid", {})
                try:
                    for box_obj in doc.boxes:
                        b_uid = _get_box_uid(box_obj)
                        if b_uid not in modified_uids:
                            continue
                        orig_key = orig_by_uid.get(b_uid, box_obj.clean_text)
                        self.sync_manager.find_and_update(
                            japanese_key=orig_key,
                            new_english_text=box_obj.clean_text,
                            search_roots=self.xuat_search_roots,
                            backup=True,
                            backup_dir=backup_dir,
                        )
                except Exception as e:
                    self.logger.warning("UI / Theme / Config", f"Secondary XUAT sync failed for inactive doc: {e}")

            self._refresh_opened_files_list()
            return True
        except Exception as exc:
            self.logger.exception(f"Failed saving document entry '{cur_p}':", exc)
            return False

    def on_reload(self) -> None:
        if self.current_file_path:
            self.open_file(self.current_file_path, reload_from_disk=True)

    # -------------------------------------------------------------------------
    # Search Engine, Background Worker & Substring Result Highlighting
    # -------------------------------------------------------------------------
    def on_start_search(self) -> None:
        if getattr(self, "_is_searching", False) and getattr(self, "_search_thread", None) and self._search_thread.is_alive():
            return

        query = self.search_var.get().strip()
        if not query:
            self._is_searching = False
            return

        if self.var_regex.get():
            try:
                flags = 0 if self.var_case.get() else re.IGNORECASE
                re.compile(query, flags)
            except re.error as e:
                self._is_searching = False
                messagebox.showerror("Search", f"Invalid regular expression:\n{e}")
                return

        opts = SearchOptions(
            query=query,
            match_case=self.var_case.get(),
            use_regex=self.var_regex.get(),
            ignore_whitespace=self.var_ignore_ws.get(),
            include_bundles=self.var_inc_bundles.get(),
            include_text=self.var_inc_text.get()
        )
        self.active_search_options = opts

        scope = self.scope_var.get()
        target_paths: List[Path] = []

        if scope == "current":
            if getattr(self, "open_documents", None):
                target_paths = list(self.open_documents.keys())
            elif self.current_file_path:
                target_paths = [self.current_file_path]
            else:
                self._is_searching = False
                messagebox.showinfo("Search", "No file is currently open.")
                return
        elif scope == "folder":
            ent_val = self.folder_path_var.get().strip() if hasattr(self, "folder_path_var") else ""
            if ent_val and Path(ent_val).is_dir():
                self.selected_search_folder = Path(ent_val)
            if self.selected_search_folder and self.selected_search_folder.is_dir():
                target_paths = [self.selected_search_folder]
            else:
                fld = filedialog.askdirectory(title="Select Folder to Search In")
                if not fld:
                    self._is_searching = False
                    return
                self.selected_search_folder = Path(fld)
                self.folder_path_var.set(str(fld))
                target_paths = [self.selected_search_folder]
        else:
            ent_val = self.folder_path_var.get().strip() if hasattr(self, "folder_path_var") else ""
            if ent_val and Path(ent_val).is_dir():
                self._set_project_folder(Path(ent_val))
            active_proj = getattr(self, "project_folder", None) or getattr(self, "bepinex_project_folder", None)
            target_paths = self._resolve_project_search_roots(active_proj)

        self._reset_search_results_state()
        self._switch_dock_tab("search")
        self.lbl_results_title.config(text="Searching...")
        self.btn_find.config(state="disabled")
        self.btn_cancel.config(state="normal")
        self.progress_bar.pack(fill="x", padx=8, pady=(0, 2))
        self.progress_bar["value"] = 0
        self.search_cancel_flag = False
        self._search_seq = getattr(self, "_search_seq", 0) + 1
        current_seq = self._search_seq
        self._is_searching = True
        self.logger.info("Search", f"Started search query='{query}' scope={scope} roots={len(target_paths)}")

        mem_docs: Dict[Path, Any] = {}
        skip_paths: set = set()
        initial_skipped: List[Tuple[Path, str]] = []

        if getattr(self, "open_documents", None):
            for fp, entry in self.open_documents.items():
                resolved_fp = Path(fp).resolve()
                if isinstance(entry, dict):
                    if entry.get("doc"):
                        orig_doc = entry["doc"]
                        # Capture immutable snapshot on UI thread before thread start (Rule 15 / SEARCH-RACE)
                        try:
                            snap_records = [
                                Record(cmd_id=r.cmd_id, cmd_name=r.cmd_name, args=list(r.args), category=r.category)
                                for r in orig_doc.records
                            ]
                            mem_docs[resolved_fp] = StoryDocument(snap_records)
                        except Exception as ex:
                            self.logger.warning("Search", f"Failed to snapshot open document {fp}: {ex}")
                            # Grok-E02: NEVER pass live orig_doc; isolate and skip
                            skip_paths.add(resolved_fp)
                            skip_paths.add(Path(fp))
                            initial_skipped.append((Path(fp), f"Snapshot error: {ex}"))
                    elif entry.get("plain_text") is not None:
                        txt_val = str(entry["plain_text"])
                        mem_docs[resolved_fp] = txt_val

        target_fn = self._run_background_search
        try:
            import inspect
            eff = getattr(target_fn, "side_effect", None)
            fn_to_check = eff if callable(eff) else target_fn
            sig = inspect.signature(fn_to_check)
            params = list(sig.parameters.values())
            has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params)
            has_varkw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params)

            if has_varargs or len(params) >= 6:
                t_args = (target_paths, opts, mem_docs, current_seq, skip_paths, initial_skipped)
                t_kwargs = {}
            elif has_varkw:
                t_args = (target_paths, opts, mem_docs)
                t_kwargs = {"search_seq": current_seq, "skip_paths": skip_paths, "initial_skipped": initial_skipped}
            else:
                avail_args = [target_paths, opts, mem_docs, current_seq, skip_paths, initial_skipped]
                t_args = tuple(avail_args[:len(params)])
                t_kwargs = {}
        except Exception:
            t_args = (target_paths, opts, mem_docs, current_seq, skip_paths, initial_skipped)
            t_kwargs = {}

        t = threading.Thread(
            target=target_fn,
            args=t_args,
            kwargs=t_kwargs,
            daemon=True
        )
        self._search_thread = t
        t.start()

    def _reset_search_results_state(self) -> None:
        self.active_search_results.clear()
        self.search_file_groups.clear()
        self._file_group_lookup.clear()
        self._result_line_map.clear()
        self._result_idx_to_line.clear()
        self._selected_result_idx = None

        self.txt_results.config(state="normal")
        self.txt_results.delete("1.0", tk.END)
        self.txt_results.config(state="disabled")

    def on_cancel_search(self) -> None:
        self.search_cancel_flag = True
        self._is_searching = False
        self.btn_cancel.config(state="disabled")
        self.lbl_status.config(text="Cancelling search...")
        self.logger.info("Search", "Search cancelled by user.")

    def _run_background_search(
        self,
        paths: List[Path],
        options: SearchOptions,
        mem_docs: Optional[Dict[Path, Any]] = None,
        search_seq: int = 1,
        skip_paths: Optional[set] = None,
        initial_skipped: Optional[List[Tuple[Path, str]]] = None,
    ) -> None:
        """Executed inside a background daemon thread (Rule 15, Part B.8)."""
        total_found = 0
        skipped_entries: List[Tuple[Path, str]] = list(initial_skipped or [])

        def on_prog(cur, tot, filename):
            self.search_queue.put(("progress", cur, tot, filename, search_seq))

        def on_err(fp, reason):
            skipped_entries.append((Path(fp), str(reason)))

        try:
            for target in paths:
                if self.search_cancel_flag:
                    break
                try:
                    if not target.exists():
                        skipped_entries.append((Path(target), "Path not found"))
                        continue
                    if target.is_file():
                        resolved_target = target.resolve()
                        if skip_paths and (target in skip_paths or resolved_target in skip_paths):
                            continue
                        mem_doc = None
                        if mem_docs:
                            mem_doc = mem_docs.get(target) or mem_docs.get(resolved_target)
                        results = self.search_engine.search_file(target, options, doc=mem_doc, on_error=on_err)
                    else:
                        results = self.search_engine.search_directory(
                            target, options, recursive=True,
                            on_progress=on_prog,
                            should_cancel=lambda: self.search_cancel_flag,
                            in_memory_docs=mem_docs,
                            on_error=on_err,
                            skip_paths=skip_paths,
                        )
                    total_found += len(results)
                    self.search_queue.put(("batch", results, search_seq))
                except Exception as ex:
                    skipped_entries.append((Path(target), str(ex)))
        finally:
            self.search_queue.put(("finished", total_found, skipped_entries, search_seq))

    def _process_search_queue(self) -> None:
        """Polls results from background worker thread and renders highlighted hits."""
        try:
            while True:
                msg = self.search_queue.get_nowait()
                kind = msg[0]

                # Drop stale search messages (BUG-22)
                seq = None
                if kind == "batch" and len(msg) >= 3:
                    seq = msg[2]
                elif kind == "progress" and len(msg) >= 5:
                    seq = msg[4]
                elif kind == "finished" and len(msg) >= 4:
                    seq = msg[3]

                if seq is not None and hasattr(self, "_search_seq") and seq != self._search_seq:
                    continue

                if kind == "progress":
                    _, cur, tot, fname, *_ = msg
                    if tot > 0:
                        pct = int((cur / tot) * 100)
                        self.progress_bar["value"] = pct
                        self.lbl_status.config(text=f"Searching ({cur}/{tot}): {fname}")

                elif kind == "batch":
                    batch_results: List[SearchResult] = msg[1]
                    if batch_results:
                        for r in batch_results:
                            res_idx = len(self.active_search_results)
                            self.active_search_results.append(r)
                            fkey = str(r.file_path)
                            grp = self._file_group_lookup.get(fkey)
                            if grp is None:
                                grp = {
                                    "key": fkey,
                                    "path": r.file_path,
                                    "collapsed": False,
                                    "indices": [],
                                }
                                self._file_group_lookup[fkey] = grp
                                self.search_file_groups.append(grp)
                            grp["indices"].append(res_idx)
                        self._render_search_results()

                elif kind == "finished":
                    self._is_searching = False
                    total = len(self.active_search_results)
                    skipped = msg[2] if len(msg) > 2 else []
                    skip_count = len(skipped)
                    is_cancelled = getattr(self, "search_cancel_flag", False)

                    if is_cancelled:
                        skip_info = f" ({skip_count} skipped)" if skip_count else ""
                        self.lbl_results_title.config(text=f"Search Cancelled ({total} matches{skip_info})")
                        self.lbl_status.config(text=f"Search cancelled. Found {total} matches{skip_info}.")
                    elif total == 0:
                        if skip_count:
                            self.lbl_results_title.config(text=f"Search Results (0 matches, {skip_count} skipped)")
                            self.lbl_status.config(text=f"Search complete. 0 matches ({skip_count} skipped).")
                        else:
                            self.lbl_results_title.config(text="Search Results (0 matches)")
                            self.lbl_status.config(text="Search complete. No matches found.")
                    else:
                        skip_info = f" ({skip_count} skipped)" if skip_count else ""
                        self.lbl_results_title.config(text=f"Search Results ({total} matches{skip_info})")
                        self.lbl_status.config(text=f"Search complete. Found {total} matches{skip_info}.")

                    self.btn_find.config(state="normal")
                    self.btn_cancel.config(state="disabled")
                    self.progress_bar.pack_forget()
                    if skipped:
                        formatted_skipped = [
                            f"{p.name if isinstance(p, Path) else p} ({reason})"
                            if isinstance(item, tuple) and len(item) == 2 and (p := item[0], reason := item[1])
                            else str(item)
                            for item in skipped
                        ]
                        self.logger.warning("Search", f"Skipped inaccessible paths: {', '.join(formatted_skipped)}")
                    self.logger.info("Search", f"Search finished. Total matches={total}, skipped={skip_count}")
                    if not self.var_preview_compiled.get():
                        if self.var_continuous_view.get():
                            self._highlight_continuous_matches()
                        else:
                            self._highlight_dialogue_matches()

        except queue.Empty:
            pass

        try:
            if getattr(self, "_destroyed", False) or not self.winfo_exists():
                return
            self._search_poll_job = self.after(100, self._process_search_queue)
        except Exception:
            pass

