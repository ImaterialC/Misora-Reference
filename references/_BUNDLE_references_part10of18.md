# BUNDLE references (10/18) | Files: references/misora_parts/misora_part07_L08652-L10142.py

--- FILE: references/misora_parts/misora_part07_L08652-L10142.py [PART 2 | L1428-1494/1494 | SHA:3b5811c48b88] ---
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

    def _on_toggle_card_lock(self, box_idx: int) -> None:
        """Toggle Translation Lock on a specific dialogue box card."""
        if not self.current_doc or not self.current_doc.boxes:
            return
        if not (0 <= box_idx < len(self.current_doc.boxes)):
            return
        self.current_box_idx = box_idx
        self.is_box0_active = False
        self.on_toggle_lock_current_box()

