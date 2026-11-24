# ======================================================================
# FILE: misora.py — PART 06 / 10
# ORIGINAL LINE RANGE : L6653 .. L7933 (total 1281 lines of 12835)
# SOURCE SHA-256      : d23baae2be82fe93a18da7d3769af30d19ebe02a8b5f6a3645d56a6f53c0710e
# NOTE FOR AI REVIEWER: Cite ORIGINAL line numbers (L6653..L7933) and symbol names.
# SYMBOLS IN THIS PART (with exact original line numbers):
#   L06653:   MisoraApp.open_file (def)
#   L06861:   MisoraApp._update_views (def)
#   L07016:   MisoraApp._update_raw_view (def)
#   L07055:   MisoraApp._flush_continuous_card_edits (def)
#   L07122:   MisoraApp._on_card_text_edited (def)
#   L07197:   MisoraApp._on_card_focus_in (def)
#   L07210:   MisoraApp._clear_card_registry (def)
#   L07226:   MisoraApp._highlight_active_card_header (def)
#   L07248:   MisoraApp._sync_header_controls_for_card (def)
#   L07282:   MisoraApp._copy_single_card_dialogue (def)
#   L07290:   MisoraApp._card_shortcut_wrap (def)
#   L07302:   MisoraApp._highlight_ngui_tags_for_widget (def)
#   L07312:   MisoraApp.on_copy_script (def)
#   L07327:   MisoraApp._on_cont_mousewheel (def)
#   L07335:   MisoraApp._resize_cont_canvas (def)
#   L07344:   MisoraApp._on_toggle_select_box_mode (def)
#   L07353:   MisoraApp._on_toggle_pin_speaker (def)
#   L07368:   MisoraApp.on_select_whole_story (def)
#   L07384:   MisoraApp.on_text_cut (def)
#   L07397:   MisoraApp.on_text_copy (def)
#   L07407:   MisoraApp.on_text_paste (def)
#   L07420:   MisoraApp._push_undo (def)
#   L07428:   MisoraApp._mark_document_dirty (def)
#   L07442:   MisoraApp._dirty_state_changed (def)
#   L07468:   MisoraApp._record_saved_checkpoint (def)
#   L07490:   MisoraApp._evaluate_checkpoints_for_op (def)
#   L07552:   MisoraApp._sync_clean_view_to_current_box (def)
#   L07592:   MisoraApp.on_box_new (def)
#   L07624:   MisoraApp.on_box_copy (def)
#   L07652:   MisoraApp.on_box_cut (def)
#   L07693:   MisoraApp.on_box_paste (def)
#   L07776:   MisoraApp._on_card_paste_caret (def)
#   L07898:   MisoraApp._on_size_dropdown_clicked (def)
#   L07913:   MisoraApp.on_insert_font_size (def)
# ======================================================================

    def open_file(self, file_path: Union[str, Path], reload_from_disk: bool = False) -> None:
        """Open and display a .unity3d bundle or plain-text script file."""
        file_path = Path(file_path).resolve()
        if not file_path.is_file():
            self.logger.error("File I/O", f"Cannot find file: {file_path}")
            messagebox.showerror("File Error", f"Cannot find file: {file_path}")
            return

        staged = None
        ext = file_path.suffix.lower()

        # Cache-hit switches do not need a disk load, but still flush the old
        # editor context after staging/target resolution succeeds.
        if not reload_from_disk and file_path in self.open_documents:
            entry = self.open_documents[file_path]
            staged = {
                "kind": "cache",
                "entry": entry,
                "doc": entry.get("doc"),
                "env": entry.get("env"),
                "obj": entry.get("obj"),
                "is_bundle": entry.get("is_bundle", False),
                "dirty": entry.get("dirty", False),
                "plain_text": entry.get("plain_text", ""),
                "status": f"Switched to {file_path.name}",
            }
        elif ext in (".unity3d", ".asset"):
            try:
                doc, env, obj, asset_name = load_bundle_story(file_path)
                staged = {
                    "kind": "bundle",
                    "doc": doc,
                    "env": env,
                    "obj": obj,
                    "asset_name": asset_name,
                    "is_bundle": True,
                    "dirty": False,
                    "plain_text": "",
                    "status": (
                        f"Loaded Bundle: {file_path.name} ({asset_name}) | "
                        f"Size: {file_path.stat().st_size / 1024:.1f} KB | "
                        f"{len(doc.boxes)} dialogue boxes"
                    ),
                    "cache": {
                        "doc": doc,
                        "env": env,
                        "obj": obj,
                        "is_bundle": True,
                        "dirty": False,
                        "plain_text": "",
                        "boxes_count": len(doc.boxes),
                    },
                }
            except Exception as e:
                self.logger.exception(f"Failed to open bundle '{file_path.name}':", e)
                messagebox.showerror("Bundle Load Error", f"Failed to open '{file_path.name}':\n{e}")
                return
        else:
            try:
                decoded = read_text_file_strictly(file_path)
                content = decoded.text
                if content.startswith("#!priconne-story"):
                    doc = StoryDocument.from_v2_text(content)
                    staged = {
                        "kind": "v2",
                        "doc": doc,
                        "env": None,
                        "obj": None,
                        "is_bundle": False,
                        "dirty": False,
                        "plain_text": "",
                        "status": f"Loaded Script: {file_path.name} | {len(doc.boxes)} dialogue boxes",
                        "cache": {
                            "doc": doc,
                            "env": None,
                            "obj": None,
                            "is_bundle": False,
                            "dirty": False,
                            "plain_text": "",
                            "boxes_count": len(doc.boxes),
                            "encoding": decoded.encoding,
                            "has_bom": decoded.has_bom,
                            "newline": decoded.newline,
                        },
                    }
                else:
                    staged = {
                        "kind": "text",
                        "doc": None,
                        "env": None,
                        "obj": None,
                        "is_bundle": False,
                        "dirty": False,
                        "plain_text": content,
                        "status": f"Opened Text File: {file_path.name}",
                        "cache": {
                            "doc": None,
                            "env": None,
                            "obj": None,
                            "is_bundle": False,
                            "dirty": False,
                            "plain_text": content,
                            "boxes_count": 0,
                            "encoding": decoded.encoding,
                            "has_bom": decoded.has_bom,
                            "newline": decoded.newline,
                        },
                    }
            except Exception as e:
                self.logger.exception(f"Failed to read '{file_path.name}':", e)
                messagebox.showerror("File Load Error", f"Failed to read '{file_path.name}':\n{e}")
                return

        # Flush the previous context only after the target is ready. Resolve
        # the actual editor widget explicitly; focus must not decide this switch.
        if not self._flush_active_widget():
            return

        self._save_active_document_state()

        doc = staged["doc"]
        is_bundle = staged["is_bundle"]
        plain_text = staged["plain_text"]

        self.current_file_path = file_path
        if hasattr(self, "undo_journal") and hasattr(self.undo_journal, "set_active_file"):
            self.undo_journal.set_active_file(str(file_path))
        self.current_doc = doc
        self.current_unity_env = staged["env"]
        self.current_text_obj = staged["obj"]
        self.is_bundle_file = is_bundle
        self._plain_text_content = plain_text

        if staged["kind"] == "cache":
            entry = staged["entry"]
            self.is_dirty = bool(entry.get("dirty", False))
            self.current_box_idx = int(entry.get("current_box_idx", 0))
            self.is_box0_active = bool(entry.get("is_box0_active", False))
            self._locked_box_uids = set(entry.get("locked_box_uids", set()))
            self._modified_box_uids = set(entry.get("modified_box_uids", set()))
            self._original_jp_by_uid = dict(entry.get("original_jp_by_uid", {}))
        else:
            self.current_box_idx = 0
            self.is_box0_active = False
            self.is_dirty = staged["dirty"]
            self._locked_box_uids = set()
            self._modified_box_uids = set()
            self._original_jp_by_uid = (
                {_get_box_uid(b): b.clean_text for b in doc.boxes if _get_box_uid(b) is not None}
                if doc is not None and doc.boxes
                else {}
            )
            staged_cache = staged.get("cache")
            if staged_cache is not None:
                staged_cache["current_box_idx"] = 0
                staged_cache["is_box0_active"] = False
                staged_cache["locked_box_uids"] = set()
                staged_cache["modified_box_uids"] = set()
                staged_cache["original_jp_by_uid"] = dict(self._original_jp_by_uid)

        if doc is not None and doc.boxes:
            self.current_box_idx = max(0, min(self.current_box_idx, len(doc.boxes) - 1))
            self._locked_boxes = {i for i, b in enumerate(doc.boxes) if _get_box_uid(b) in self._locked_box_uids}
            self._modified_boxes = {i for i, b in enumerate(doc.boxes) if _get_box_uid(b) in self._modified_box_uids}
            self._original_box_texts = {i: self._original_jp_by_uid.get(_get_box_uid(b), b.clean_text) for i, b in enumerate(doc.boxes)}
            for b in doc.boxes:
                b_uid = _get_box_uid(b)
                if b_uid is not None and b_uid not in self._original_jp_by_uid:
                    self._original_jp_by_uid[b_uid] = b.clean_text
        else:
            self.current_box_idx = 0
            self._locked_boxes = set()
            self._modified_boxes = set()
            self._original_box_texts = {}

        if hasattr(self, "recent_files"):
            if file_path in self.recent_files:
                self.recent_files.remove(file_path)
        else:
            self.recent_files = []
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:15]
        self.last_opened_dir = file_path.parent
        self.title(f"Misora Editor - {file_path.name}")

        if staged["kind"] == "cache":
            entry = staged["entry"]
            self.is_dirty = bool(entry.get("dirty", False))
        else:
            self.open_documents[file_path] = staged["cache"]
            # Record a fresh saved-state checkpoint for newly loaded documents
            self._record_saved_checkpoint(file_path, staged.get("doc"), staged.get("plain_text", ""))

        self._update_views()
        self._dirty_state_changed()
        self._sync_edit_menu_states()
        self.lbl_status.config(text=staged["status"])

        if staged["kind"] == "bundle":
            self.logger.info(
                "File I/O",
                f"Opened bundle '{file_path}' (asset={staged['asset_name']}, boxes={len(doc.boxes)})",
            )
        elif staged["kind"] == "v2":
            self.logger.info("File I/O", f"Opened v2 script '{file_path}' (boxes={len(doc.boxes)})")
        elif staged["kind"] == "text":
            self.logger.info("File I/O", f"Opened plain text file '{file_path}' ({len(plain_text)} chars)")

    def _update_views(self) -> None:
        """Update Game Display View (Page or Continuous, Raw or Compiled Preview) and Raw AST View."""
        compiled = self.var_preview_compiled.get()

        if not self.current_doc:
            self._clear_card_registry()  # S4: prune stale card refs on plain-text / empty state
            self.speaker_var.set("")
            self.lbl_box_counter.config(text="Box: 0 / 0")
            self.lbl_voice_cue.config(text="")

            self.txt_dialogue.config(state="normal")
            self.txt_dialogue.delete("1.0", tk.END)
            if compiled:
                self._insert_compiled_ngui_text(self.txt_dialogue, "1.0", self._plain_text_content)
                self.txt_dialogue.config(state="disabled")
            else:
                self.txt_dialogue.insert("1.0", self._plain_text_content)
                self._highlight_ngui_tags()
                self._highlight_dialogue_matches()
            self._auto_resize_dialogue_box()

            self.txt_continuous.config(state="normal")
            self.txt_continuous.delete("1.0", tk.END)
            if compiled:
                self._insert_compiled_ngui_text(self.txt_continuous, "1.0", self._plain_text_content)
                self.txt_continuous.config(state="disabled")
            else:
                self.txt_continuous.insert("1.0", self._plain_text_content)
                self._highlight_ngui_tags()
                self._highlight_continuous_matches()

            try:
                self.txt_raw.config(state="normal")
                self.txt_raw.delete("1.0", tk.END)
                if self.current_file_path:
                    self.txt_raw.insert("1.0", f"(Plain text file: {self.current_file_path})")
            finally:
                self.txt_raw.config(state="disabled")
            return

        if not self.current_doc.boxes:
            self.speaker_var.set("")
            self.lbl_voice_cue.config(text="")
            self.txt_dialogue.config(state="normal")
            self.txt_dialogue.delete("1.0", tk.END)
            self.txt_continuous.config(state="normal")
            self.txt_continuous.delete("1.0", tk.END)
            try:
                self.txt_raw.config(state="normal")
                self.txt_raw.delete("1.0", tk.END)
            finally:
                self.txt_raw.config(state="disabled")
            self.lbl_box_counter.config(text="Box: 0 / 0")
            self._auto_resize_dialogue_box()
            return

        if self.is_box0_active:
            if not self.current_doc or not self.current_doc.has_metadata():
                self.is_box0_active = False
            else:
                total_boxes = len(self.current_doc.boxes)
                self.speaker_var.set("")
                if hasattr(self, "entry_speaker"):
                    self.entry_speaker.config(state="disabled")
                if hasattr(self, "btn_speaker_dropdown"):
                    self.btn_speaker_dropdown.config(state="disabled")
                self.lbl_box_counter.config(text=f"Box: 0 / {total_boxes} (Story Metadata)")
                self.lbl_voice_cue.config(text="")
                if hasattr(self, "btn_prev"):
                    self.btn_prev.config(state="disabled")
                if hasattr(self, "btn_next"):
                    self.btn_next.config(state="normal" if total_boxes > 0 else "disabled")

                if self.var_continuous_view.get():
                    self._render_continuous_view()
                    self._focus_continuous_box(-1, move_cursor=True)
                else:
                    if hasattr(self, "clean_editor_row") and self._is_widget_packed(self.clean_editor_row):
                        self.clean_editor_row.pack_forget()
                    if hasattr(self, "ruler_clean") and self._is_widget_packed(self.ruler_clean):
                        self.ruler_clean.pack_forget()
                    if hasattr(self, "panel_box0_metadata") and not self._is_widget_packed(self.panel_box0_metadata):
                        self.panel_box0_metadata.pack(fill="both", expand=True)

                    meta = self.current_doc.get_metadata()
                    self.var_box0_title.set(meta.get("title", ""))
                    self.var_box0_subtitle.set(meta.get("subtitle", ""))
                    self.txt_box0_summary.delete("1.0", tk.END)
                    self.txt_box0_summary.insert("1.0", meta.get("summary", ""))
                    self._update_box0_char_counter()
                    self.gd_canvas.yview_moveto(0.0)

                self._update_raw_view()
                if hasattr(self, "_translator_dialog") and self._translator_dialog and self._translator_dialog.winfo_exists():
                    self._translator_dialog.refresh_box()
                return

        if hasattr(self, "panel_box0_metadata") and self._is_widget_packed(self.panel_box0_metadata):
            self.panel_box0_metadata.pack_forget()
        if hasattr(self, "clean_editor_row") and not self._is_widget_packed(self.clean_editor_row):
            if self.show_column_ruler and hasattr(self, "ruler_clean") and not self._is_widget_packed(self.ruler_clean):
                try:
                    self.ruler_clean.pack(before=self.clean_editor_row, side="top", fill="x", pady=(0, 2))
                except Exception:
                    self.ruler_clean.pack(side="top", fill="x", pady=(0, 2))
            self.clean_editor_row.pack(fill="both", expand=True)

        total_boxes = len(self.current_doc.boxes)
        self.current_box_idx = max(0, min(self.current_box_idx, total_boxes - 1))
        box = self.current_doc.boxes[self.current_box_idx]

        if hasattr(self, "entry_speaker"):
            self.entry_speaker.config(state="normal")
        if hasattr(self, "btn_speaker_dropdown"):
            self.btn_speaker_dropdown.config(state="normal")
        self.speaker_var.set(box.speaker)
        self.lbl_box_counter.config(text=f"Box: {self.current_box_idx + 1} / {total_boxes}")
        self.lbl_voice_cue.config(text=f"Voice Cue: {box.voice_cue}" if box.voice_cue else "")

        if hasattr(self, "btn_lock_box"):
            is_locked = self.current_box_idx in self._locked_boxes
            self.btn_lock_box.config(
                text="🔒" if is_locked else "🔓",
                bg=self.theme["accent_yellow"] if is_locked else self.theme["bg_panel"]
            )
        self._update_rendered_char_count(box.clean_text)

        if hasattr(self, "btn_prev"):
            can_prev = (self.current_box_idx > 0) or (self.current_doc and self.current_doc.has_metadata())
            self.btn_prev.config(state="normal" if can_prev else "disabled")
        if hasattr(self, "btn_next"):
            self.btn_next.config(state="normal" if self.current_box_idx < total_boxes - 1 else "disabled")

        if self.var_continuous_view.get():
            self._render_continuous_view()
            self._focus_continuous_box(self.current_box_idx, move_cursor=True)
        else:
            self.txt_dialogue.config(state="normal")
            self.txt_dialogue.delete("1.0", tk.END)
            if compiled:
                self._insert_compiled_ngui_text(self.txt_dialogue, "1.0", box.clean_text)
                self.txt_dialogue.config(state="disabled")
            else:
                self.txt_dialogue.insert("1.0", box.clean_text)
                self._highlight_ngui_tags()
                self._highlight_dialogue_matches()
                self._highlight_secret_whitespace(self.txt_dialogue)
            self._update_gutter_clean()
            self.gd_canvas.yview_moveto(0.0)
            self._auto_resize_dialogue_box()

        self._update_raw_view()
        if hasattr(self, "_translator_dialog") and self._translator_dialog and self._translator_dialog.winfo_exists():
            self._translator_dialog.refresh_box()

    def _update_raw_view(self) -> None:
        """Render Raw AST View and highlight records associated with current_box_idx or Box 0."""
        self.txt_raw.config(state="normal")
        try:
            self.txt_raw.delete("1.0", tk.END)
            if not self.current_doc:
                return

            active_rec_indices = set()
            if getattr(self, "is_box0_active", False) and self.current_doc:
                for idx, r in enumerate(self.current_doc.records):
                    if (r.cmd_id == 0 and len(r.args) > 0 and r.args[0]) or \
                       (r.cmd_id == 32 and len(r.args) > 0 and r.args[0]) or \
                       (r.cmd_id == 1 and len(r.args) > 0 and r.args[0]):
                        active_rec_indices.add(idx)
            elif self.current_doc and self.current_doc.boxes and 0 <= self.current_box_idx < len(self.current_doc.boxes):
                active_box = self.current_doc.boxes[self.current_box_idx]
                active_uids = {s.record.uid for s in active_box.segs}
                active_rec_indices = {i for i, r in enumerate(self.current_doc.records) if r.uid in active_uids}

            raw_lines = []
            first_active_line = None
            for i, r in enumerate(self.current_doc.records):
                args_str = "  ".join(f"'{a}'" for a in r.args)
                is_active = i in active_rec_indices
                if is_active and first_active_line is None:
                    first_active_line = i + 1
                marker = " >> " if is_active else "    "
                raw_lines.append(f"{marker}[{i:03d}] {r.cmd_name:<14} {args_str}")

            self.txt_raw.insert("1.0", "\n".join(raw_lines))
            if first_active_line is not None:
                self.txt_raw.see(f"{first_active_line}.0")
        finally:
            self.txt_raw.config(state="disabled")

    # -------------------------------------------------------------------------
    # Continuous View: Box Card Stream Architecture & Two-Way Sync
    # -------------------------------------------------------------------------
    def _flush_continuous_card_edits(self) -> None:
        """Flush any uncommitted edits from active Box Cards or plain text back into model."""
        if not self.current_doc:
            if hasattr(self, "txt_continuous") and self.txt_continuous.winfo_exists():
                if not getattr(self, "var_preview_compiled", None) or not self.var_preview_compiled.get():
                    new_tx = self.txt_continuous.get("1.0", "end-1c")
                    if self._plain_text_content != new_tx:
                        old_tx = self._plain_text_content
                        self.undo_journal.record(
                            PlainTextDelta(
                                file_path=str(self.current_file_path or ""),
                                old_content=old_tx,
                                new_content=new_tx,
                            ),
                            label=f"Edit {self.current_file_path.name if self.current_file_path else 'text'}"
                        )
                        self._plain_text_content = new_tx
                        if self.current_file_path and self.current_file_path in self.open_documents:
                            self.open_documents[self.current_file_path]["plain_text"] = new_tx
                        self._mark_document_dirty(self.current_file_path)
            return

        if not getattr(self, "_card_widgets", None):
            return

        for b_idx, card_info in list(self._card_widgets.items()):
            if b_idx == -1:
                continue
            if 0 <= b_idx < len(self.current_doc.boxes):
                txt_w = card_info.get("txt")
                if txt_w and txt_w.winfo_exists():
                    new_tx = txt_w.get("1.0", "end-1c")
                    box = self.current_doc.boxes[b_idx]
                    if box.clean_text != new_tx:
                        old_sp = box.speaker
                        old_tx = box.clean_text
                        box_uid = box.segs[0].record.uid if box.segs else None
                        old_segs = [s.text for s in box.segs] if len(box.segs) > 1 else None
                        try:
                            self.current_doc.inject_box(b_idx, None, new_tx)
                        except Exception as e:
                            self.logger.exception(f"Failed to flush card edit for box {b_idx}:", e)
                            self.set_status(f"Error flushing box #{b_idx + 1}: {e}", is_error=True)
                            continue

                        new_segs = None
                        if old_segs is not None:
                            refreshed_box = next((b for b in self.current_doc.boxes if b.segs and b.segs[0].record.uid == box_uid), None)
                            if refreshed_box:
                                new_segs = [s.text for s in refreshed_box.segs]

                        delta = BoxEditDelta(
                            box_index=b_idx,
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
                        self.undo_journal.record(delta, label=f"Edit box #{b_idx + 1}")
                        self._modified_boxes.add(b_idx)
                        self._mark_document_dirty(self.current_file_path)

    def _on_card_text_edited(self, box_idx: int, txt_w: tk.Text, gutter: Optional[tk.Text] = None) -> bool:
        """Handle inline typing inside a Box Card. Returns True if content was mutated (BUG-30)."""
        if getattr(self, "_suppress_continuous_events", False) or self.var_preview_compiled.get():
            return False
        if not self.current_doc or not (0 <= box_idx < len(self.current_doc.boxes)):
            return False

        new_tx = txt_w.get("1.0", "end-1c")
        box = self.current_doc.boxes[box_idx]
        mutated = False
        if box.clean_text != new_tx:
            old_sp = box.speaker
            old_tx = box.clean_text
            box_uid = box.segs[0].record.uid if box.segs else None
            old_segs = [s.text for s in box.segs] if len(box.segs) > 1 else None
            try:
                self.current_doc.inject_box(box_idx, None, new_tx)
            except Exception as e:
                self.logger.exception(f"Failed to inject box {box_idx}:", e)
                self.set_status(f"Error updating box #{box_idx + 1}: {e}", is_error=True)
                return False

            new_segs = None
            if old_segs is not None:
                refreshed_box = next((b for b in self.current_doc.boxes if b.segs and b.segs[0].record.uid == box_uid), None)
                if refreshed_box:
                    new_segs = [s.text for s in refreshed_box.segs]

            delta = BoxEditDelta(
                box_index=box_idx,
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
            self.undo_journal.record(delta, label=f"Edit box #{box_idx + 1}")
            self._modified_boxes.add(box_idx)
            self._mark_document_dirty(self.current_file_path)
            try:
                self._update_raw_view()
                if box_idx == getattr(self, "current_box_idx", -1):
                    self._update_rendered_char_count(new_tx)
            except Exception:
                pass
            mutated = True

        # Dynamically adjust text widget height to fit content (min 2, max 10)
        line_count = max(1, new_tx.count("\n") + 1)
        eff_height = max(2, min(10, line_count))
        try:
            if int(txt_w.cget("height")) != eff_height:
                txt_w.config(height=eff_height)
        except Exception:
            pass

        if gutter:
            try:
                gutter.config(state="normal", height=eff_height)
                gutter.delete("1.0", tk.END)
                gutter.insert("1.0", "\n".join(str(n) for n in range(1, line_count + 1)))
                gutter.config(state="disabled")
            except Exception:
                pass

        if hasattr(self, "cont_canvas"):
            self.cont_canvas.configure(scrollregion=self.cont_canvas.bbox("all"))

        self._highlight_ngui_tags_for_widget(txt_w)
        return mutated

    def _on_card_focus_in(self, box_idx: int) -> None:
        """Update active indicators and controls when a Box Card gains focus."""
        if getattr(self, "_suppress_continuous_events", False) or not self.current_doc:
            return

        self.is_box0_active = (box_idx == -1)
        if box_idx != -1 and 0 <= box_idx < len(self.current_doc.boxes):
            self.current_box_idx = box_idx

        self._highlight_active_card_header(box_idx)
        self._sync_header_controls_for_card(box_idx)
        self._update_raw_view()

    def _clear_card_registry(self) -> None:
        """Destroy and prune all stale card widget references (S4 / STALE-CARD-REGISTRY).

        Safe to call even if widgets are already destroyed. Clears _card_widgets entirely.
        Must be called whenever the document that produced the cards is unloaded so that
        destroyed Tk widget references do not persist in the registry (Rule 3 / Rule 11).
        """
        for _b_idx, card_info in list(self._card_widgets.items()):
            card = card_info.get("card")
            try:
                if card is not None and card.winfo_exists():
                    card.destroy()
            except Exception:
                pass
        self._card_widgets.clear()

    def _highlight_active_card_header(self, active_idx: int) -> None:
        """Highlight the header background of the active card in Continuous View."""
        t = self.theme
        if not hasattr(self, "_card_widgets"):
            return
        for b_idx, card_info in self._card_widgets.items():
            hdr = card_info.get("hdr")
            if not hdr or not hdr.winfo_exists():
                continue
            is_active = (b_idx == active_idx)
            if b_idx == -1:
                bg_col = t["highlight_bg"] if is_active else ("#dfd1f5" if self._is_light_theme() else "#2d1d29")
            else:
                bg_col = t["highlight_bg"] if is_active else t["bg_panel"]
            try:
                hdr.configure(bg=bg_col)
                for child in hdr.winfo_children():
                    if isinstance(child, (tk.Label, tk.Frame)):
                        child.configure(bg=bg_col)
            except Exception:
                pass

    def _sync_header_controls_for_card(self, box_idx: int) -> None:
        """Sync top ribbon controls (speaker, voice cue, box counter) to active card."""
        if not self.current_doc:
            return
        total = len(self.current_doc.boxes) if self.current_doc.boxes else 0
        if box_idx == -1:
            if not (self._is_speaker_pinned and self.speaker_var.get()):
                self.speaker_var.set("")
            if hasattr(self, "entry_speaker"):
                self.entry_speaker.config(state="disabled")
            if hasattr(self, "btn_speaker_dropdown"):
                self.btn_speaker_dropdown.config(state="disabled")
            self.lbl_box_counter.config(text=f"Box: 0 / {total} (Story Metadata)")
            self.lbl_voice_cue.config(text="")
            if hasattr(self, "btn_prev"):
                self.btn_prev.config(state="disabled")
            if hasattr(self, "btn_next"):
                self.btn_next.config(state="normal" if total > 0 else "disabled")
        elif 0 <= box_idx < total:
            box = self.current_doc.boxes[box_idx]
            if hasattr(self, "entry_speaker"):
                self.entry_speaker.config(state="normal")
            if hasattr(self, "btn_speaker_dropdown"):
                self.btn_speaker_dropdown.config(state="normal")
            if not (self._is_speaker_pinned and self.speaker_var.get()):
                self.speaker_var.set(box.speaker)
            self.lbl_box_counter.config(text=f"Box: {box_idx + 1} / {total}")
            self.lbl_voice_cue.config(text=f"Voice Cue: {box.voice_cue}" if box.voice_cue else "")
            if hasattr(self, "btn_prev"):
                can_prev = (box_idx > 0) or (self.current_doc and self.current_doc.has_metadata())
                self.btn_prev.config(state="normal" if can_prev else "disabled")
            if hasattr(self, "btn_next"):
                self.btn_next.config(state="normal" if box_idx < total - 1 else "disabled")

    def _copy_single_card_dialogue(self, box_idx: int) -> None:
        """Copy dialogue from a single Box Card to clipboard."""
        if self.current_doc and 0 <= box_idx < len(self.current_doc.boxes):
            text = self.current_doc.boxes[box_idx].clean_text
            self.clipboard_clear()
            self.clipboard_append(text)
            self.show_toast(f"📋 Copied dialogue from Box #{box_idx + 1}")

    def _card_shortcut_wrap(self, w: tk.Text, open_t: str, close_t: str) -> None:
        """Wrap selected text in card editor with NGUI tags."""
        try:
            sel_first = w.index("sel.first")
            sel_last = w.index("sel.last")
            txt = w.get(sel_first, sel_last)
            w.delete(sel_first, sel_last)
            w.insert(sel_first, f"{open_t}{txt}{close_t}")
        except tk.TclError:
            w.insert(tk.INSERT, f"{open_t}{close_t}")
        self._commit_widget_edit(w)

    def _highlight_ngui_tags_for_widget(self, w: tk.Text) -> None:
        """Syntax-color NGUI tags within a specific Text widget."""
        if self.var_preview_compiled.get() or not w.winfo_exists():
            return
        w.tag_remove("ngui_tag", "1.0", tk.END)
        tx = w.get("1.0", "end-1c")
        for m in NGUI_TAG_RE.finditer(tx):
            w.tag_add("ngui_tag", f"1.0 + {m.start()}c", f"1.0 + {m.end()}c")
        w.tag_raise("ngui_tag")

    def on_copy_script(self) -> None:
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
        """Toggle multi-box selection mode in continuous view and update UI."""
        enabled = bool(self.var_select_box_mode.get())
        if not enabled:
            self._selected_boxes.clear()
        if self.var_continuous_view.get():
            self._render_continuous_view()
        self.show_toast(f"Select Box mode {'enabled' if enabled else 'disabled'}")

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

    def on_select_whole_story(self) -> None:
        """Select whole story / all text across document."""
        if self.var_continuous_view.get():
            if hasattr(self, "_card_widgets") and self._card_widgets:
                first_card = self._card_widgets.get(0) or self._card_widgets.get(-1)
                if first_card and "txt" in first_card:
                    txt = first_card["txt"]
                    txt.focus_set()
                    txt.tag_add("sel", "1.0", "end-1c")
            self.show_toast("Selected active story")
        else:
            if hasattr(self, "txt_dialogue"):
                self.txt_dialogue.focus_set()
                self.txt_dialogue.tag_add("sel", "1.0", "end-1c")
                self.show_toast("Selected all text in current box")

    def on_text_cut(self) -> None:
        """Cut text in active editor to clipboard."""
        target = self.txt_dialogue
        if self.var_continuous_view.get() and hasattr(self, "_card_widgets") and self.current_box_idx in self._card_widgets:
            target = self._get_card_text_widget(self.current_box_idx)
        self._current_edit_source = "cut"
        try:
            target.event_generate("<<Cut>>")
        except Exception:
            pass
        finally:
            self._current_edit_source = "keyboard"

    def on_text_copy(self) -> None:
        """Copy text in active editor to clipboard."""
        target = self.txt_dialogue
        if self.var_continuous_view.get() and hasattr(self, "_card_widgets") and self.current_box_idx in self._card_widgets:
            target = self._get_card_text_widget(self.current_box_idx)
        try:
            target.event_generate("<<Copy>>")
        except Exception:
            pass

    def on_text_paste(self) -> None:
        """Paste text in active editor with delimiter-awareness."""
        target = self.txt_dialogue
        idx = self.current_box_idx
        if self.var_continuous_view.get() and hasattr(self, "_card_widgets") and self.current_box_idx in self._card_widgets:
            target = self._get_card_text_widget(self.current_box_idx)
        res = self._on_card_paste_caret(idx, target)
        if res != "break":
            try:
                target.event_generate("<<Paste>>")
            except Exception:
                pass

    def _push_undo(self, label: str = "Edit") -> None:
        """Fallback hook for callers expecting _push_undo; structural handlers record typed deltas."""
        pass

    # -------------------------------------------------------------------------
    # S2: Per-Document Dirty Contract Helpers
    # -------------------------------------------------------------------------

    def _mark_document_dirty(self, file_path: Optional[Union[str, Path]]) -> None:
        """Flag-only dirty marker — ZERO Tk calls, ZERO dock/title rebuilds (Rule 13 / S2).

        Mutates only open_documents[path]["dirty"] and self.is_dirty.
        Safe to call from worker threads (BatchTranslateDialog.worker) provided ZERO Tk ops follow.
        """
        if not file_path:
            return
        p = Path(file_path).resolve()
        if p in self.open_documents:
            self.open_documents[p]["dirty"] = True
        if self.current_file_path and Path(self.current_file_path).resolve() == p:
            self.is_dirty = True

    def _dirty_state_changed(self) -> None:
        """Pure UI synchronization: title *, Opened Files dock, undo/redo menu states (S2).

        Mirrors self.is_dirty from open_documents[path]["dirty"] when the active document is cached.
        When the active path is NOT in open_documents (e.g., test_34 synthetic tmp path), PRESERVES
        the current self.is_dirty value unchanged.
        Calls _refresh_opened_files_list() exactly once.
        NEVER derives dirty state from undo_journal.is_clean() — that was the cross-file clobber bug.
        """
        if self.current_file_path:
            p = Path(self.current_file_path).resolve()
            if p in self.open_documents:
                # Mirror from authoritative per-document entry
                self.is_dirty = bool(self.open_documents[p].get("dirty", False))
            # If NOT in open_documents: preserve self.is_dirty unchanged (do not reset to False)

        dirty_marker = "*" if self.is_dirty else ""
        file_name = self.current_file_path.name if self.current_file_path else "Untitled"
        try:
            self.title(f"Misora Editor - {file_name}{dirty_marker}")
        except Exception:
            pass

        self._refresh_opened_files_list()
        self._sync_edit_menu_states()

    def _record_saved_checkpoint(self, file_path: Optional[Union[str, Path]],
                                  doc: Optional[Any], plain_text: str = "") -> None:
        """Record saved-state fingerprint for a document (S2 / Rule 13).

        Story docs: SHA-256 of doc.to_v2_text(). Plain-text: SHA-256 of plain_text.
        Called at: open_file() fresh load, open_file() reload_from_disk=True, on_save() primary success.
        Never mutates dirty flags; purely stores a comparison baseline.
        """
        if not file_path:
            return
        key = str(Path(file_path).resolve())
        try:
            if doc is not None:
                content = doc.to_v2_text()
            else:
                content = plain_text
            self._saved_state_checkpoints[key] = hashlib.sha256(
                content.encode("utf-8", errors="replace")
            ).hexdigest()
        except Exception:
            pass

    def _evaluate_checkpoints_for_op(self, op: Any) -> None:
        """After undo/redo delta loop: compare live fingerprints to saved checkpoints (S2).

        For each path touched by the op:
        - If a checkpoint exists and the live fingerprint matches → mark clean.
        - If no checkpoint exists → leave dirty as set by _mark_document_dirty (never clear speculatively).
        """
        touched: set = set()
        for delta in op.deltas:
            fp = getattr(delta, "file_path", None)
            if fp:
                try:
                    touched.add(Path(fp).resolve())
                except Exception:
                    pass
            elif hasattr(delta, "per_file"):
                for item in delta.per_file:
                    try:
                        fpath_str = item[0]
                        touched.add(Path(fpath_str).resolve())
                    except Exception:
                        pass
        if self.current_file_path:
            try:
                touched.add(Path(self.current_file_path).resolve())
            except Exception:
                pass

        for p in touched:
            key = str(p)
            entry = self.open_documents.get(p)
            if entry is not None:
                if key not in self._saved_state_checkpoints:
                    # No baseline — cannot determine clean; leave dirty flag as-is
                    continue
                saved_fp = self._saved_state_checkpoints[key]
                try:
                    doc = entry.get("doc")
                    if doc is not None:
                        live_content = doc.to_v2_text()
                    else:
                        live_content = entry.get("plain_text", "")
                    live_fp = hashlib.sha256(live_content.encode("utf-8", errors="replace")).hexdigest()
                except Exception:
                    continue

                is_clean = (live_fp == saved_fp)
                entry["dirty"] = not is_clean
                if self.current_file_path:
                    try:
                        if Path(self.current_file_path).resolve() == p:
                            self.is_dirty = not is_clean
                    except Exception:
                        pass
            elif self.current_file_path:
                try:
                    if Path(self.current_file_path).resolve() == p and hasattr(self, "undo_journal"):
                        is_clean = self.undo_journal.is_clean(p)
                        self.is_dirty = not is_clean
                except Exception:
                    pass

    def _sync_clean_view_to_current_box(self) -> None:
        """
        Synchronize Page View dialogue and header controls to current_box_idx
        without tearing down the entire Continuous View canvas.
        """
        if not self.current_doc or not self.current_doc.boxes:
            return
        total = len(self.current_doc.boxes)
        self.current_box_idx = max(0, min(self.current_box_idx, total - 1))
        box = self.current_doc.boxes[self.current_box_idx]

        if hasattr(self, "speaker_var"):
            self.speaker_var.set(box.speaker)
        if hasattr(self, "lbl_box_counter"):
            self.lbl_box_counter.config(text=f"Box: {self.current_box_idx + 1} / {total}")
        if hasattr(self, "lbl_voice_cue"):
            self.lbl_voice_cue.config(text=f"Voice Cue: {box.voice_cue}" if box.voice_cue else "")
        if hasattr(self, "lbl_segs_badge"):
            self.lbl_segs_badge.config(text=f"{len(box.segs)} segs" if len(box.segs) > 1 else "")

        if hasattr(self, "txt_dialogue") and self.txt_dialogue.winfo_exists() and not self.var_continuous_view.get():
            self.txt_dialogue.config(state="normal")
            self.txt_dialogue.delete("1.0", tk.END)
            if self.var_preview_compiled.get():
                self._insert_compiled_ngui_text(self.txt_dialogue, "1.0", box.clean_text)
                self.txt_dialogue.config(state="disabled")
            else:
                self.txt_dialogue.insert("1.0", box.clean_text)
                self._highlight_ngui_tags()
                self._highlight_dialogue_matches()
            self._auto_resize_dialogue_box()

        if hasattr(self, "btn_prev"):
            can_prev = (self.current_box_idx > 0) or (self.current_doc and self.current_doc.has_metadata())
            self.btn_prev.config(state="normal" if can_prev else "disabled")
        if hasattr(self, "btn_next"):
            self.btn_next.config(state="normal" if self.current_box_idx < total - 1 else "disabled")

        self._update_raw_view()

    def on_box_new(self) -> None:
        """Create and insert a new dialogue box after current box."""
        if not self.current_doc:
            self.show_toast("No story document loaded")
            return

        cur_sp = self.speaker_var.get() if (self._is_speaker_pinned and self.speaker_var.get()) else ""
        ins_idx = self.current_box_idx + 1 if self.current_doc.boxes else 0
        new_snap = BoxSnapshot(
            speaker=cur_sp,
            voice_cue="",
            kind="print" if cur_sp else "tag",
            seg_texts=[""],
        )
        self.current_doc.insert_box(ins_idx, new_snap)
        self.undo_journal.record(
            BoxStructuralDelta(
                op_type="insert",
                box_index=ins_idx,
                snapshots=[new_snap],
                file_path=str(self.current_file_path or ""),
            ),
            label="New Box"
        )
        self.current_box_idx = ins_idx
        self._mark_document_dirty(self.current_file_path)
        self._modified_boxes.add(ins_idx)
        self._render_continuous_view()
        self._sync_clean_view_to_current_box()
        self._dirty_state_changed()
        self.show_toast(f"➕ Created new Box #{ins_idx + 1}")

    def on_box_copy(self) -> None:
        """Copy selected box(es) or current box to box clipboard using CSIF format (Part C.1)."""
        if not self.current_doc or not self.current_doc.boxes:
            self.show_toast("No story document loaded")
            return
        self._commit_widget_edit()
        targets = sorted(self._selected_boxes) if self._selected_boxes else [self.current_box_idx]
        targets = [idx for idx in targets if 0 <= idx < len(self.current_doc.boxes)]
        if not targets:
            return

        include_meta = "auto"
        if getattr(self, "is_box0_active", False) or (-1 in getattr(self, "_selected_boxes", set())):
            include_meta = True

        csif_str = serialize(
            self.current_doc,
            scope="selection",
            box_indices=targets,
            include_metadata=include_meta
        )

        self._box_clipboard = [BoxSnapshot.from_box(self.current_doc.boxes[idx]) for idx in targets]
        self._box_clipboard_text = csif_str
        self.safe_clipboard_set(csif_str)
        self.show_toast(f"📋📦 Copied {len(targets)} box(es) (CSIF)")
        self.lbl_status.config(text=f"Copied {len(targets)} box(es) in CSIF format to clipboard")

    def on_box_cut(self) -> None:
        """Cut selected box(es) or current box in one undo batch."""
        if not self.current_doc or not self.current_doc.boxes:
            self.show_toast("No story document loaded")
            return
        raw_targets = sorted(self._selected_boxes) if self._selected_boxes else [self.current_box_idx]
        raw_targets = [idx for idx in raw_targets if 0 <= idx < len(self.current_doc.boxes)]
        if not raw_targets:
            return

        unlocked_targets = [idx for idx in raw_targets if not self.is_box_locked(idx)]
        locked_count = len(raw_targets) - len(unlocked_targets)
        if locked_count > 0:
            self.show_toast(f"🔒 Skipped {locked_count} locked box(es).")
        if not unlocked_targets:
            return

        targets = unlocked_targets
        self._selected_boxes = set(targets)
        self.on_box_copy()
        deleted_snapshots = self.current_doc.delete_boxes(targets)
        self.undo_journal.record(
            BoxStructuralDelta(
                op_type="delete",
                box_index=targets[0],
                snapshots=deleted_snapshots,
                indices=list(targets),
                file_path=str(self.current_file_path or ""),
            ),
            label="Cut Box(es)"
        )
        self._selected_boxes.clear()
        self._resync_box_indices_from_uids()
        if self.current_box_idx >= len(self.current_doc.boxes):
            self.current_box_idx = max(0, len(self.current_doc.boxes) - 1)
        self._mark_document_dirty(self.current_file_path)
        self._dirty_state_changed()
        self._render_continuous_view()
        self._sync_clean_view_to_current_box()
        self.show_toast(f"✂📦 Cut {len(targets)} box(es)")

    def on_box_paste(self, confirm: bool = True) -> None:
        """Paste box(es) from clipboard as new boxes after current box (Part C.2)."""
        if not self.current_doc:
            self.show_toast("No story document loaded")
            return

        clip_text = self.safe_clipboard_get()
        if getattr(self, "_box_clipboard_text", None) != clip_text:
            self._box_clipboard = None
            self._box_clipboard_text = None

        snaps_to_ins: List[BoxSnapshot] = []
        if getattr(self, "_box_clipboard", None):
            snaps_to_ins = [
                BoxSnapshot(
                    speaker=snap.speaker,
                    voice_cue=snap.voice_cue,
                    kind=snap.kind,
                    seg_texts=list(snap.seg_texts),
                    extra_args=[list(ea) for ea in snap.extra_args] if snap.extra_args else None,
                )
                for snap in self._box_clipboard
            ]
        elif clip_text.strip():
            result = parse(clip_text)
            parsed_blocks = result.blocks
            if parsed_blocks:
                snaps_to_ins = [
                    BoxSnapshot(
                        speaker="" if b.is_narration else b.speaker,
                        voice_cue="",
                        kind="tag" if (b.is_narration or not b.speaker) else "print",
                        seg_texts=[b.text]
                    )
                    for b in parsed_blocks
                ]

        if not snaps_to_ins:
            self.show_toast("Box clipboard is empty")
            return

        ins_idx = self.current_box_idx + 1 if self.current_doc.boxes else 0
        block_count = len(snaps_to_ins)
        first_speakers = [
            (s.speaker if s.speaker else "(Narration)")
            for s in snaps_to_ins[:3]
        ]
        sp_desc = ", ".join(first_speakers)
        if block_count > 3:
            sp_desc += f", ... (+{block_count - 3} more)"

        if confirm:
            ins_desc = f"after Box #{self.current_box_idx + 1}" if self.current_doc.boxes else "at beginning"
            msg = f"Insert {block_count} box(es) {ins_desc}?\n\nSpeakers: {sp_desc}"
            ans = messagebox.askyesno("Paste Box(es)", msg, parent=self)
            if not ans:
                return

        self.undo_journal.begin_batch(f"Paste {block_count} Box(es)")
        try:
            for offset, snap in enumerate(snaps_to_ins):
                target_idx = ins_idx + offset
                self.current_doc.insert_box(target_idx, snap)
                self._modified_boxes.add(target_idx)

            self.undo_journal.record(
                BoxStructuralDelta(
                    op_type="insert",
                    box_index=ins_idx,
                    snapshots=snaps_to_ins,
                    file_path=str(self.current_file_path or ""),
                )
            )
        finally:
            self.undo_journal.end_batch()

        self.current_box_idx = ins_idx + len(snaps_to_ins) - 1
        self._mark_document_dirty(self.current_file_path)
        self._dirty_state_changed()
        self._render_continuous_view()
        self._sync_clean_view_to_current_box()
        self.show_toast(f"📥📦 Pasted {len(snaps_to_ins)} box(es)")

    def _on_card_paste_caret(self, box_idx: int, txt_widget: tk.Text) -> str:
        """Intercept paste on card editors to perform caret-aware paste or CSIF handling."""
        clip_text = self.safe_clipboard_get()
        if not clip_text:
            return ""

        if sniff_format(clip_text) == "csif":
            self._handle_editor_csif_paste(txt_widget, clip_text)
            return "break"

        if "\n\n\n" not in clip_text:
            return ""

        chunks = clip_text.split("\n\n\n")
        if len(chunks) <= 1:
            return ""

        try:
            sel_ranges = txt_widget.tag_ranges("sel")
            if sel_ranges:
                head = txt_widget.get("1.0", sel_ranges[0])
                tail = txt_widget.get(sel_ranges[1], "end-1c")
            else:
                ins = txt_widget.index("insert")
                head = txt_widget.get("1.0", ins)
                tail = txt_widget.get(ins, "end-1c")
        except Exception:
            head = txt_widget.get("1.0", "end-1c")
            tail = ""

        if not self.current_doc or not self.current_doc.boxes:
            return "break"

        # Check if all target boxes are locked (Technical Guard 2 / BUG-10)
        total_boxes = len(self.current_doc.boxes)
        targets_to_mutate = []
        for offset in range(len(chunks)):
            t_idx = box_idx + offset
            if t_idx < total_boxes:
                if not self.is_box_locked(t_idx):
                    targets_to_mutate.append(t_idx)
            else:
                targets_to_mutate.append(t_idx)

        if not targets_to_mutate:
            self.show_toast("🔒 All target boxes are locked against edits.")
            return "break"

        mutated_count = 0
        self.undo_journal.begin_batch("Multi-box Delimiter Paste")
        try:
            if not self.is_box_locked(box_idx):
                b0 = self.current_doc.boxes[box_idx]
                first_text = head + chunks[0]
                self.current_doc.inject_box(box_idx, None, first_text)
                self.undo_journal.record(
                    BoxEditDelta(
                        box_index=box_idx,
                        old_speaker=b0.speaker,
                        new_speaker=b0.speaker,
                        old_text=b0.clean_text,
                        new_text=first_text,
                        file_path=str(self.current_file_path or ""),
                        box_uid=b0.uid,
                        source="paste_caret",
                    )
                )
                self._modified_boxes.add(box_idx)
                mutated_count += 1

            for offset, chunk in enumerate(chunks[1:], start=1):
                target_idx = box_idx + offset
                if target_idx < len(self.current_doc.boxes) and self.is_box_locked(target_idx):
                    continue
                is_last = (offset == len(chunks) - 1)
                if target_idx < len(self.current_doc.boxes):
                    orig_b = self.current_doc.boxes[target_idx]
                    orig_text = orig_b.clean_text
                    new_text = (chunk + tail + orig_text) if is_last else (chunk + orig_text)
                    self.current_doc.inject_box(target_idx, None, new_text)
                    self.undo_journal.record(
                        BoxEditDelta(
                            box_index=target_idx,
                            old_speaker=orig_b.speaker,
                            new_speaker=orig_b.speaker,
                            old_text=orig_text,
                            new_text=new_text,
                            file_path=str(self.current_file_path or ""),
                            box_uid=orig_b.uid,
                            source="paste_caret",
                        )
                    )
                    self._modified_boxes.add(target_idx)
                    mutated_count += 1
                else:
                    new_text = (chunk + tail) if is_last else chunk
                    snap = BoxSnapshot(speaker="", voice_cue="", kind="tag", seg_texts=[new_text])
                    self.current_doc.insert_box(target_idx, snap)
                    self.undo_journal.record(
                        BoxStructuralDelta(
                            op_type="insert",
                            box_index=target_idx,
                            snapshots=[snap],
                            file_path=str(self.current_file_path or ""),
                        )
                    )
                    self._modified_boxes.add(target_idx)
                    mutated_count += 1
        finally:
            self.undo_journal.end_batch()

        if mutated_count > 0:
            self._resync_box_indices_from_uids()
            self._mark_document_dirty(self.current_file_path)
            self._dirty_state_changed()
            self._render_continuous_view()
            self._sync_clean_view_to_current_box()
            self.show_toast(f"Pasted across {mutated_count} box(es)")
        else:
            self.show_toast("🔒 Target box(es) were locked; no edits applied.")
        return "break"

    def _on_size_dropdown_clicked(self) -> None:
        """Show dropdown menu for selecting font size scaling tags."""
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Small (80%)", command=lambda: self.on_insert_font_size("80%"))
        menu.add_command(label="Normal (100% / Reset)", command=lambda: self.on_insert_font_size(None))
        menu.add_command(label="Large (130%)", command=lambda: self.on_insert_font_size("130%"))
        menu.add_command(label="Extra Large / Roar (160%)", command=lambda: self.on_insert_font_size("160%"))
        menu.add_command(label="Huge (200%)", command=lambda: self.on_insert_font_size("200%"))
        try:
            x = self.winfo_pointerx()
            y = self.winfo_pointery()
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    def on_insert_font_size(self, size_val: Optional[str]) -> None:
        """Insert font size tags (<size=...>...</size>) around selection or at caret."""
        target = self.txt_dialogue
        if self.var_continuous_view.get() and hasattr(self, "_card_widgets") and self.current_box_idx in self._card_widgets:
            target = self._card_widgets[self.current_box_idx].get("txt", self.txt_dialogue)

        if size_val:
            open_t = f"<size={size_val}>"
            close_t = "</size>"
            try:
                sel_first = target.index("sel.first")
                sel_last = target.index("sel.last")
                sel_txt = target.get(sel_first, sel_last)
                target.delete(sel_first, sel_last)
                target.insert(sel_first, f"{open_t}{sel_txt}{close_t}")
            except tk.TclError:
                target.insert(tk.INSERT, f"{open_t}{close_t}")
                target.mark_set(tk.INSERT, f"{tk.INSERT} - {len(close_t)}c")
        else:
            target.insert(tk.INSERT, "</size>")

