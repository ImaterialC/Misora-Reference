# BUNDLE references (9/18) | Files: references/misora_parts/misora_part07_L08652-L10142.py

--- FILE: references/misora_parts/misora_part07_L08652-L10142.py [PART 1 | L1-1427/1494 | SHA:3b5811c48b88] ---
# misora.py PART 07/12 | ORIG L8652-L10142/17315 | SHA:ec4d9bfc8ec6
# SYMS: L8652:MisoraApp.on_select_whole_story, L8668:MisoraApp.on_text_cut, L8681:MisoraApp.on_text_copy, L8691:MisoraApp.on_text_paste, L8704:MisoraApp._push_undo, L8712:MisoraApp._mark_document_dirty, L8726:MisoraApp._dirty_state_changed, L8752:MisoraApp._record_saved_checkpoint, L8774:MisoraApp._evaluate_checkpoints_for_op, L8836:MisoraApp._sync_clean_view_to_current_box, L8877:MisoraApp.on_box_new, L8909:MisoraApp.on_box_copy, L8937:MisoraApp.on_box_cut, L8978:MisoraApp.on_box_paste, L9061:MisoraApp._on_card_paste_caret, L9183:MisoraApp._on_size_dropdown_clicked, L9198:MisoraApp.on_insert_font_size, L9226:MisoraApp._render_continuous_view, L9595:MisoraApp._focus_continuous_box, L9649:MisoraApp._find_continuous_box_at_index, L9655:MisoraApp._nearest_continuous_box_to_index, L9659:MisoraApp._on_continuous_cursor_moved, L9663:MisoraApp._on_continuous_key_guard, L9667:MisoraApp._on_continuous_copy, L9671:MisoraApp._on_continuous_paste_guard, L9675:MisoraApp._on_continuous_cut_guard, L9679:MisoraApp._on_continuous_key_release, L9683:MisoraApp._sync_continuous_box_from_widget, L9687:MisoraApp._highlight_dialogue_matches, L9721:MisoraApp._highlight_continuous_matches, L9749:MisoraApp._commit_speaker_edit, L9818:MisoraApp._on_speaker_edited, L9822:MisoraApp._refresh_continuous_box_header, L9837:MisoraApp._on_dialogue_key_up, L9847:MisoraApp._on_dialogue_key_down, L9857:MisoraApp._commit_widget_edit, L9955:MisoraApp._on_dialogue_edited, L10040:MisoraApp._update_box0_char_counter, L10050:MisoraApp._on_box0_metadata_edited, L10088:MisoraApp.on_prev_box, L10108:MisoraApp.on_next_box, L10125:MisoraApp.is_box_locked, L10133:MisoraApp._on_toggle_card_lock

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
        self._update_dialogue_select_box_ui()

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
        self._update_views()
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
        self._update_views()
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
        if not getattr(self, "is_box0_active", False) and self.current_doc and self.is_box_locked(self.current_box_idx):
            self.show_toast(f"Box #{self.current_box_idx + 1} is locked.")
            return

        target = self.txt_dialogue
        if self.var_continuous_view.get() and hasattr(self, "_card_widgets") and self.current_box_idx in self._card_widgets:
            target = self._get_card_text_widget(self.current_box_idx)

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

        target.focus_set()
        self._commit_widget_edit(target)

    def _render_continuous_view(self) -> None:
        """Render all dialogue boxes sequentially as a Box Card Stream."""
        compiled = self.var_preview_compiled.get()
        self._suppress_continuous_events = True
        t = self.theme
        d_fam = getattr(self, "dialogue_font_family", self.prefs.get("dialogue_font_family", "Consolas"))
        d_sz = int(getattr(self, "dialogue_font_size", self.prefs.get("dialogue_font_size", 11)))
        safe_w = self._measure_dialogue_metrics("")["safe_w"] if compiled else 0

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

                slot_cb_0 = tk.Frame(hdr_0, width=22, height=18, bg=box0_bg)
                slot_cb_0.pack_propagate(False)
                slot_cb_0.pack(side="left", padx=(0, 2))
                cb_sel_0 = None
                if self.var_select_box_mode.get():
                    var_box0_sel = tk.BooleanVar(master=self, value=(-1 in self._selected_boxes))
                    def _make_box0_sel_cmd(v):
                        def _cmd():
                            if v.get():
                                self._selected_boxes.add(-1)
                            else:
                                self._selected_boxes.discard(-1)
                        return _cmd
                    cb_sel_0 = tk.Checkbutton(
                        slot_cb_0,
                        variable=var_box0_sel,
                        command=_make_box0_sel_cmd(var_box0_sel),
                        bg=box0_bg,
                        activebackground=box0_bg,
                        selectcolor=t["bg_panel"],
                        bd=0,
                        cursor="hand2",
                    )
                    cb_sel_0.pack(fill="both", expand=True)
                    cb_sel_0.bind("<MouseWheel>", self._on_cont_mousewheel)

                slot_lock_0 = tk.Frame(hdr_0, width=18, height=18, bg=box0_bg)
                slot_lock_0.pack_propagate(False)
                slot_lock_0.pack(side="left", padx=(0, 2))

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
                    "slot_cb": slot_cb_0,
                    "cb_sel": cb_sel_0,
                }

            # 2. Cards #1..N: Dialogue Box Cards
            cream_bg = "#fffcf4"
            outer_gold = "#d4af37"
            inner_gold = "#e6c875"
            plate_bg = "#3b2c4e"
            plate_fg = best_contrast_fg(plate_bg, "#ffffff", "#fffcf4")
            preview_fg = best_contrast_fg(cream_bg, "#2b2118", "#1a1a1a")
            arrow_fg = "#ff5c93"

            for i, box in enumerate(self.current_doc.boxes):
                is_active = (not getattr(self, "is_box0_active", False) and i == self.current_box_idx)
                if compiled:
                    hdr_bg = "#f4e7c3" if is_active else cream_bg
                    card_frame = tk.Frame(self.cont_stream_frame, bg=outer_gold, padx=2, pady=2)
                    inner_card = tk.Frame(
                        card_frame,
                        bg=cream_bg,
                        highlightbackground=inner_gold,
                        highlightthickness=1,
                        padx=6,
                        pady=4,
                    )
                    inner_card.pack(fill="both", expand=True)
                    hdr = tk.Frame(inner_card, bg=hdr_bg, padx=4, pady=2)
                else:
                    hdr_bg = t["highlight_bg"] if is_active else t["bg_panel"]
                    card_frame = tk.Frame(self.cont_stream_frame, bg=t["bg_panel"])
                    inner_card = card_frame
                    hdr = tk.Frame(card_frame, bg=hdr_bg, padx=4, pady=0)

                # Fixed reserved checkbox slot (prevents header shift when Select Box toggles)
                slot_cb = tk.Frame(hdr, width=22, height=18, bg=hdr_bg)
                slot_cb.pack_propagate(False)
                slot_cb.pack(side="left", padx=(0, 2))

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
                        slot_cb,
                        variable=var_box_sel,
                        command=_make_box_sel_cmd(i, var_box_sel),
                        bg=hdr_bg,
                        activebackground=hdr_bg,
                        selectcolor=t["bg_panel"],
                        bd=0,
                        cursor="hand2",
                    )
                    cb_sel.pack(fill="both", expand=True)
                    cb_sel.bind("<MouseWheel>", self._on_cont_mousewheel)

                # Translation Lock indicator immediately to the RIGHT of checkbox slot (fixed width=2)
                is_locked = i in getattr(self, "_locked_boxes", set())
                lbl_lock = tk.Label(
                    hdr,
                    text="🔒" if is_locked else "",
                    font=("Segoe UI", max(7, d_sz - 4)),
                    fg=t["accent_yellow"],
                    bg=hdr_bg,
                    width=2,
                    cursor="hand2",
                )
                lbl_lock.pack(side="left", padx=(0, 2))
                lbl_lock.bind("<Button-1>", lambda e, b_idx=i: self._on_toggle_card_lock(b_idx))
                lbl_lock.bind("<MouseWheel>", self._on_cont_mousewheel)
                create_tooltip(lbl_lock, "Click to toggle Translation Lock (Ctrl+L)")

                lbl_badge = tk.Label(
                    hdr,
                    text=f"◆ [BOX #{i+1:03d}]",
                    font=("Consolas", max(8, d_sz - 3), "bold"),
                    fg=best_contrast_fg(hdr_bg, t["misora_pink"], "#7a1c4b") if compiled else t["misora_pink"],
                    bg=hdr_bg,
                )
                lbl_badge.pack(side="left")

                sp_text = box.speaker if box.speaker else "(Narration)"
                if compiled:
                    lbl_sp = tk.Label(
                        hdr,
                        text=sp_text,
                        font=(d_fam, max(8, d_sz - 2), "bold" if box.speaker else "italic"),
                        fg=plate_fg,
                        bg=plate_bg,
                        padx=6,
                        pady=1,
                    )
                else:
                    sp_fg = t["fg_text"] if box.speaker else t["fg_muted"]
                    sp_font = (d_fam, max(8, d_sz - 3), "bold" if box.speaker else "italic")
                    lbl_sp = tk.Label(hdr, text=sp_text, font=sp_font, fg=sp_fg, bg=hdr_bg)
                lbl_sp.pack(side="left", padx=(6, 4))

                vc_text = f"♪ {box.voice_cue}" if box.voice_cue else ""
                lbl_vc = tk.Label(hdr, text=vc_text, font=("Segoe UI", max(7, d_sz - 4)), fg=t["accent_blue"], bg=hdr_bg)
                lbl_vc.pack(side="left", padx=(2, 4))

                if len(box.segs) > 1:
                    lbl_segs = tk.Label(hdr, text=f"{len(box.segs)} segs", font=("Segoe UI", max(7, d_sz - 4), "bold"), fg=t["misora_pink"], bg=hdr_bg)
                    lbl_segs.pack(side="left", padx=(2, 4))

                hdr.pack(fill="x", pady=0)

                # Editor Row with dynamic line-number gutter (or lightweight Game-Style Preview body)
                editor_row = tk.Frame(inner_card, bg=cream_bg if compiled else t["bg_panel"])
                editor_row.pack(fill="x", padx=0, pady=0)

                line_count = max(1, box.clean_text.count("\n") + 1)
                eff_height = max(3, line_count) if compiled else max(2, min(10, line_count))

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
                self._apply_gutter_overflow_tag(gutter)
                gutter.config(state="disabled")
                if self.show_line_numbers and not compiled:
                    gutter.pack(side="left", fill="y", padx=(0, 2))

                txt = tk.Text(
                    editor_row,
                    wrap="none" if compiled else "word",
                    undo=False,
                    height=eff_height,
                    font=(d_fam, d_sz),
                    bg=cream_bg if compiled else t["bg_editor"],
                    fg=preview_fg if compiled else t["fg_text"],
                    insertbackground=t["misora_pink"],
                    selectbackground=t["highlight_bg"],
                    selectforeground=t["misora_pink"],
                    bd=0 if compiled else 1,
                    relief="flat" if compiled else "solid",
                    highlightthickness=0,
                    padx=8,
                    pady=3,
                    spacing1=2,
                    spacing3=2
                )
                self._configure_editor_rich_tags(txt, d_fam, d_sz)
                if compiled:
                    self._insert_compiled_ngui_text(txt, "1.0", box.clean_text)
                    self._apply_overflow_highlights(txt)
                    txt.config(state="disabled")
                else:
                    txt.insert("1.0", box.clean_text)
                    self._highlight_ngui_tags_for_widget(txt)

                txt.pack(side="left", fill="x", expand=True)

                if compiled:
                    footer_row = tk.Frame(inner_card, bg=cream_bg)
                    footer_row.pack(fill="x", pady=(2, 0))
                    safe_bar = tk.Frame(footer_row, width=safe_w, height=2, bg=inner_gold)
                    safe_bar.pack(side="left", anchor="w")
                    lbl_arrow = tk.Label(
                        footer_row,
                        text="▼",
                        font=(d_fam, max(8, d_sz - 2), "bold"),
                        fg=arrow_fg,
                        bg=cream_bg,
                    )
                    lbl_arrow.pack(side="right", padx=(4, 2))
                    for fw in (inner_card, footer_row, safe_bar, lbl_arrow):
                        fw.bind("<MouseWheel>", self._on_cont_mousewheel)

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
                    "slot_cb": slot_cb,
                    "lbl_lock": lbl_lock,
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

