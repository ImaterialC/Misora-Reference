# BUNDLE references (12/18) | Files: references/misora_parts/misora_part08_L10143-L11633.py

--- FILE: references/misora_parts/misora_part08_L10143-L11633.py [PART 2 | L1331-1494/1494 | SHA:e73a5cd43d91] ---
            matches = matches[:count]

        res = text
        for item in reversed(matches):
            start, end = item[0], item[1]
            res = res[:start] + replacement + res[end:]
        return res, len(matches)

    def _confirm_closed_files_for_op(self, op: Any, is_undo: bool = True) -> bool:
        """Prompt before modifying closed files on disk during Undo/Redo (BUG-24 / AGENTS.md §16)."""
        if not op or not hasattr(op, "deltas"):
            return True

        closed_paths: List[Path] = []
        all_paths: List[Path] = []
        for delta in op.deltas:
            if isinstance(delta, BulkFileDelta):
                for item in delta.per_file:
                    fp = Path(item[0]).resolve()
                    all_paths.append(fp)
                    if self._find_open_doc_key(fp) is None:
                        closed_paths.append(fp)

        if not closed_paths:
            return True

        action = "Undo" if is_undo else "Redo"
        file_lines = []
        for p in all_paths:
            status = " (closed - will touch disk)" if p in closed_paths else " (open tab)"
            file_lines.append(f"  • {p.name}{status}")

        msg = (
            f"{action} across multiple files:\n\n"
            f"Operation: {getattr(op, 'label', 'Bulk Operation')}\n\n"
            f"The following {len(all_paths)} file(s) will be modified on disk,\n"
            f"including {len(closed_paths)} file(s) not currently open:\n\n"
            + "\n".join(file_lines)
            + f"\n\nProceed with {action} across these files?"
        )
        ans = messagebox.askyesno(
            f"Confirm Multi-File {action}",
            msg,
            default=messagebox.NO,
            icon=messagebox.WARNING,
        )
        return bool(ans)

    def on_replace_next(self) -> None:
        """Find and replace the next occurrence in the active file."""
        find_text = self.search_var.get()
        replace_text = self.replace_var.get()
        if not find_text:
            return

        if not self.current_file_path:
            messagebox.showinfo("Replace", "No active file open to replace in.")
            return

        match_case = bool(getattr(self, "var_case", None) and self.var_case.get())
        use_regex = bool(getattr(self, "var_regex", None) and self.var_regex.get())
        ignore_ws = bool(getattr(self, "var_ignore_ws", None) and self.var_ignore_ws.get()) if getattr(self, "var_ignore_ws", None) is not None else False

        try:
            opts = SearchOptions(
                query=find_text,
                match_case=match_case,
                use_regex=use_regex,
                ignore_whitespace=ignore_ws,
            )
            search_engine = getattr(self, "search_engine", None)
            compile_fn = search_engine._compile_matcher if search_engine else ProjectSearchEngine._compile_matcher
            matcher = compile_fn(opts)
        except Exception as e:
            self.set_status(f"Invalid search pattern: {e}", is_error=True)
            messagebox.showerror("Search Error", f"Invalid search pattern:\n{e}")
            return

        if self.current_doc and self.current_doc.boxes:
            box = self.current_doc.boxes[self.current_box_idx]
            matches = matcher(box.clean_text)
            if matches:
                if self.is_box_locked(self.current_box_idx):
                    self.show_toast(f"🔒 Box {self.current_box_idx + 1} is locked against edits.")
                else:
                    old_sp = box.speaker
                    old_tx = box.clean_text
                    box_uid = box.uid
                    old_segs = [s.text for s in box.segs] if len(box.segs) > 1 else None
                    new_tx, _ = self._apply_compiled_replacement(
                        box.clean_text, matcher, replace_text, is_regex=use_regex, ignore_ws=ignore_ws, count=1
                    )
                    try:
                        self.current_doc.inject_box(self.current_box_idx, None, new_tx)
                    except Exception as e:
                        self.logger.exception(f"Failed to replace in box {self.current_box_idx}:", e)
                        self.set_status(f"Error replacing in box #{self.current_box_idx + 1}: {e}", is_error=True)
                        return

                    new_segs = None
                    if old_segs is not None:
                        refreshed_box = next((b for b in self.current_doc.boxes if b.segs and b.segs[0].record.uid == box_uid), None)
                        if refreshed_box:
                            new_segs = [s.text for s in refreshed_box.segs]

                    self.undo_journal.record(
                        BoxEditDelta(
                            box_index=self.current_box_idx,
                            old_speaker=old_sp,
                            new_speaker=old_sp,
                            old_text=old_tx,
                            new_text=new_tx,
                            file_path=str(self.current_file_path),
                            box_uid=box.uid,
                            source="replace",
                            old_seg_texts=old_segs,
                            new_seg_texts=new_segs,
                        ),
                        label=f"Replace in box #{self.current_box_idx + 1}"
                    )
                    self._modified_boxes.add(self.current_box_idx)
                    self._mark_document_dirty(self.current_file_path)
                    self._dirty_state_changed()
                    self._update_views()
                    self.lbl_status.config(text=f"Replaced 1 occurrence in Box #{self.current_box_idx + 1}")
                    return

            total = len(self.current_doc.boxes)
            for i in range(1, total):
                next_idx = (self.current_box_idx + i) % total
                if self.is_box_locked(next_idx):
                    continue
                if matcher(self.current_doc.boxes[next_idx].clean_text):
                    self.current_box_idx = next_idx
                    self._update_views()
                    self.lbl_status.config(text=f"Found match in Box #{next_idx + 1}. Press Replace again to replace.")
                    return
            messagebox.showinfo("Replace", f"No more occurrences of '{find_text}' found.")
        elif not self.current_doc and self.current_file_path:
            cur_tx = self._plain_text_content
            matches = matcher(cur_tx)
            if matches:
                new_tx, _ = self._apply_compiled_replacement(
                    cur_tx, matcher, replace_text, is_regex=use_regex, ignore_ws=ignore_ws, count=1
                )
                self.undo_journal.record(
                    PlainTextDelta(
                        file_path=str(self.current_file_path),
                        old_content=cur_tx,
                        new_content=new_tx,
                    ),
                    label=f"Replace in {self.current_file_path.name}"
                )
                self._plain_text_content = new_tx
                matched_k = self._find_open_doc_key(self.current_file_path)
                if matched_k and matched_k in self.open_documents:
                    self.open_documents[matched_k]["plain_text"] = new_tx
                self._mark_document_dirty(self.current_file_path)
                self._dirty_state_changed()
                self._update_views()
                self.lbl_status.config(text=f"Replaced 1 occurrence in {self.current_file_path.name}")
            else:
                messagebox.showinfo("Replace", f"'{find_text}' not found in current file.")

