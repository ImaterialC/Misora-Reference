# BUNDLE references (8/18) | Files: references/misora_parts/misora_part06_L07164-L08651.py

--- FILE: references/misora_parts/misora_part06_L07164-L08651.py [PART 2 | L1407-1491/1491 | SHA:5d39497e0feb] ---
        """Copy dialogue across all boxes using CSIF format (Part C.3)."""
        if not self.current_doc or not self.current_doc.boxes:
            self.show_toast("No story document loaded")
            return

        self._commit_widget_edit()
        csif_text = serialize(self.current_doc, scope="all", include_metadata="auto")
        self.safe_clipboard_set(csif_text)
        box_count = len(self.current_doc.boxes)
        self.show_toast(f"📋 Copied {box_count} boxes (CSIF format)")
        self.lbl_status.config(text=f"Copied script ({box_count} boxes in CSIF format) to clipboard")

    on_copy_script_triple_enter = on_copy_script

    def _on_cont_mousewheel(self, event) -> str:
        """Scroll continuous stream canvas smoothly and prevent child widgets from eating the scroll event."""
        if hasattr(self, "cont_canvas") and self.cont_canvas.winfo_exists():
            delta = getattr(event, "delta", 0)
            if delta:
                self.cont_canvas.yview_scroll(int(-1 * (delta / 120)), "units")
        return "break"

    def _resize_cont_canvas(self, width: int) -> None:
        """Debounced canvas window resize to eliminate sash-drag stutter."""
        self._cont_resize_job = None
        if hasattr(self, "cont_canvas") and hasattr(self, "cont_canvas_window") and self.cont_canvas.winfo_exists():
            try:
                self.cont_canvas.itemconfig(self.cont_canvas_window, width=width)
            except Exception:
                pass

    def _on_toggle_select_box_mode(self) -> None:
        """Toggle multi-box selection mode in both Dialogue and All Script views."""
        enabled = bool(self.var_select_box_mode.get())
        if not enabled:
            self._selected_boxes.clear()
        if self.var_continuous_view.get():
            self._render_continuous_view()
            if hasattr(self, "cb_dialogue_select") and self.cb_dialogue_select.winfo_exists():
                self.cb_dialogue_select.pack_forget()
        else:
            self._update_dialogue_select_box_ui()
        self.show_toast(f"Select Box mode {'enabled' if enabled else 'disabled'}")

    def _update_dialogue_select_box_ui(self) -> None:
        """Update inline Select Box checkbox in Dialogue view header."""
        if not hasattr(self, "cb_dialogue_select") or not self.cb_dialogue_select.winfo_exists():
            return
        if not self.var_select_box_mode.get() or self.var_continuous_view.get() or not self.current_doc:
            self.cb_dialogue_select.pack_forget()
            return
        is_box0 = getattr(self, "is_box0_active", False)
        b_idx = -1 if is_box0 else self.current_box_idx
        b_num = 0 if is_box0 else (self.current_box_idx + 1)
        self.var_dialogue_box_sel.set(b_idx in self._selected_boxes)
        sel_count = len(self._selected_boxes)
        self.cb_dialogue_select.config(text=f"Select Box #{b_num} ({sel_count} selected)")
        if not self.cb_dialogue_select.winfo_ismapped():
            self.cb_dialogue_select.pack(side="left", padx=(10, 0))

    def _on_dialogue_box_sel_toggle(self) -> None:
        """Toggle selection of current box in Dialogue view."""
        is_box0 = getattr(self, "is_box0_active", False)
        b_idx = -1 if is_box0 else self.current_box_idx
        if self.var_dialogue_box_sel.get():
            self._selected_boxes.add(b_idx)
        else:
            self._selected_boxes.discard(b_idx)
        self._update_dialogue_select_box_ui()

    def _on_toggle_pin_speaker(self) -> None:
        """Toggle persistent speaker pinning across box navigation."""
        self._is_speaker_pinned = not self._is_speaker_pinned
        t = self.theme
        if self._is_speaker_pinned:
            if hasattr(self, "btn_pin_speaker"):
                self.btn_pin_speaker.config(bg=t["highlight_bg"], relief="sunken")
            sp = self.speaker_var.get()
            self.show_toast(f"📌 Speaker Pinned: '{sp}' locked across navigation")
        else:
            if hasattr(self, "btn_pin_speaker"):
                btn_bg = t.get("bg_editor", "#faf8fe")
                self.btn_pin_speaker.config(bg=btn_bg, relief="raised")
            self.show_toast("Speaker Unpinned")

