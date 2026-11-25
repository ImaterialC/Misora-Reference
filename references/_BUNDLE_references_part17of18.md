# BUNDLE references (17/18) | Files: references/misora_parts/misora_part11_L14560-L16052.py

--- FILE: references/misora_parts/misora_part11_L14560-L16052.py [PART 1 | L1-1465/1496 | SHA:4681f03bfd1c] ---
# misora.py PART 11/12 | ORIG L14560-L16052/17315 | SHA:ec4d9bfc8ec6
# SYMS: L14560:MisoraApp.on_translate_current_box, L14605:MisoraApp._poll_mtl_queue, L14707:MisoraApp.on_batch_translate, L14714:MisoraApp.on_copy_ai_prompt, L14746:MisoraApp._show_paste_preview_and_apply, L14933:MisoraApp.on_paste_cross_box, L14946:MisoraApp.on_import_script, L14988:MisoraApp._get_xuat_index_roots, L14997:MisoraApp._refresh_xuat_index_async, L15023:MisoraApp._poll_xuat_index_queue, L15047:MisoraApp._get_or_build_xuat_index, L15058:MisoraApp.on_import_from_xuat, L15083:MisoraApp.on_export_script, L15127:MisoraApp.on_clear_dialogue_skeleton, L15188:MisoraApp.on_register_unity3d_association, L15253:MisoraApp.on_about, L15268:class ScriptPastePreviewDialog, L15271:ScriptPastePreviewDialog.__init__, L15328:ScriptPastePreviewDialog._build_ui, L15464:ScriptPastePreviewDialog._populate_tree, L15505:ScriptPastePreviewDialog.on_apply, L15512:ScriptPastePreviewDialog.on_cancel, L15521:class ImportFromXUATDialog, L15528:ImportFromXUATDialog.__init__, L15555:ImportFromXUATDialog._build_ui, L15648:ImportFromXUATDialog._on_rows_configure, L15652:ImportFromXUATDialog._on_canvas_configure, L15656:ImportFromXUATDialog._on_outer_mousewheel, L15661:ImportFromXUATDialog._on_reload_index, L15665:ImportFromXUATDialog._get_immutable_jp_key, L15677:ImportFromXUATDialog._populate_rows, L15929:ImportFromXUATDialog._bind_paired_box_events, L15975:ImportFromXUATDialog._step_candidate, L15986:ImportFromXUATDialog._select_candidate, L16005:ImportFromXUATDialog._apply_conflict_scope, L16027:ImportFromXUATDialog._set_filter, L16047:ImportFromXUATDialog._format_box_list

    def on_translate_current_box(self) -> None:
        """Translate the dialogue in the active box using configured active engine (F8 / Rule 15 / BUG-27)."""
        if not self.current_doc or not self.current_doc.boxes:
            self.show_toast("No story document loaded")
            return
        b_idx = self.current_box_idx
        if b_idx < 0 or b_idx >= len(self.current_doc.boxes):
            return
        if self.is_box_locked(b_idx):
            self.show_toast(f"🔒 Box {b_idx + 1} is locked against translation edits.")
            return
        box = self.current_doc.boxes[b_idx]
        orig_text = box.clean_text.strip()
        if not orig_text:
            self.show_toast("Current box has no text to translate")
            return

        engine_name = self.mtl_config.active_engine
        self.show_toast(f"Translating Box {b_idx + 1} with {engine_name}...")
        self.lbl_status.config(text=f"Translating Box {b_idx + 1} with {engine_name}...")

        b_uid = _get_box_uid(box)
        doc_id = id(self.current_doc)
        file_path_str = str(self.current_file_path or "")
        src_hash = _hash_mtl_source(orig_text)
        self._mtl_request_seq += 1
        req_seq = self._mtl_request_seq
        req_meta = (file_path_str, doc_id, b_uid, src_hash, req_seq)

        mtl_q = self._mtl_queue

        def on_success(result: str):
            mtl_q.put(("box_success", req_meta, result, engine_name))

        def on_error(err: str):
            mtl_q.put(("box_error", req_meta, str(err), engine_name))

        translate_async(
            orig_text,
            self.mtl_config,
            on_success=on_success,
            on_error=on_error,
            xuat_cache=getattr(self, "xuat_entries", None),
        )

    def _poll_mtl_queue(self) -> None:
        """Poll queued machine translation results on the main UI thread (Rule 15 / BUG-27)."""
        if not self.winfo_exists():
            return

        try:
            while True:
                msg = self._mtl_queue.get_nowait()
                kind = msg[0]
                if kind in ("box_success", "success"):
                    if kind == "box_success":
                        _, req_meta, result, engine_name = msg
                    else:
                        _, req_meta, result = msg
                        engine_name = self.mtl_config.active_engine
                    file_path_str, doc_id, b_uid, src_hash, req_seq = req_meta

                    # Identity guard 1: Verify active document has not changed
                    if not self.current_doc or id(self.current_doc) != doc_id:
                        self.logger.info("MTL", f"Discarded stale MTL result for doc_id {doc_id} (active doc switched)")
                        continue
                    if str(self.current_file_path or "") != file_path_str:
                        self.logger.info("MTL", f"Discarded stale MTL result for path {file_path_str} (path changed)")
                        continue

                    # Identity guard 2: Re-resolve target box by box_uid
                    found_idx = None
                    if b_uid is not None:
                        for idx, b in enumerate(self.current_doc.boxes):
                            if _get_box_uid(b) == b_uid:
                                found_idx = idx
                                break
                    if found_idx is None:
                        self.logger.info("MTL", f"Discarded stale MTL result: box_uid {b_uid} not found in document")
                        continue

                    # Identity guard 3: Re-verify source text has not changed in flight
                    target_box = self.current_doc.boxes[found_idx]
                    curr_hash = _hash_mtl_source(target_box.clean_text)
                    if curr_hash != src_hash:
                        self.logger.info("MTL", f"Discarded stale MTL result: source text for box {found_idx + 1} changed in flight")
                        continue

                    # Identity guard 4: Re-verify box is not locked against edits
                    if self.is_box_locked(found_idx):
                        self.logger.info("MTL", f"Discarded MTL result: box {found_idx + 1} is locked")
                        continue

                    # Identity guard 5: Re-verify monotonic request sequence
                    latest_seq = self._latest_applied_mtl_seq.get(b_uid, 0)
                    if req_seq < latest_seq:
                        self.logger.info("MTL", f"Discarded superseded MTL seq {req_seq} < {latest_seq} for box {b_uid}")
                        continue
                    self._latest_applied_mtl_seq[b_uid] = req_seq

                    # Mutate AST first (S07 / BUG-13 mutate-before-undo)
                    old_speaker = target_box.speaker
                    old_text = target_box.clean_text
                    old_segs = [s.text for s in target_box.segs]
                    self.current_doc.inject_box(found_idx, old_speaker, result)
                    new_box = self.current_doc.boxes[found_idx]
                    new_segs = [s.text for s in new_box.segs]

                    self.undo_journal.record(
                        BoxEditDelta(
                            box_index=found_idx,
                            old_speaker=old_speaker,
                            new_speaker=old_speaker,
                            old_text=old_text,
                            new_text=result,
                            file_path=str(self.current_file_path) if self.current_file_path else "",
                            box_uid=b_uid,
                            source="mtl",
                            old_seg_texts=old_segs,
                            new_seg_texts=new_segs,
                        )
                    )
                    self._modified_boxes.add(found_idx)
                    self._mark_document_dirty(self.current_file_path)
                    self._dirty_state_changed()
                    self._update_views()
                    self.show_toast(f"✓ Translated Box {found_idx + 1} via {engine_name}")
                    self.lbl_status.config(text=f"Box {found_idx + 1} translated via {engine_name}")

                elif kind in ("box_error", "error"):
                    if kind == "box_error":
                        _, req_meta, err_str, engine_name = msg
                    else:
                        _, req_meta, err_str = msg
                        engine_name = self.mtl_config.active_engine
                    file_path_str, doc_id, b_uid, src_hash, req_seq = req_meta
                    if self.current_doc and id(self.current_doc) == doc_id:
                        self.logger.error("MTL", f"Translation failed via {engine_name}: {err_str}")
                        self.show_toast(f"❌ Translation failed: {err_str}")
                        self.lbl_status.config(text=f"Translation failed: {err_str}")

        except queue.Empty:
            pass
        finally:
            if self.winfo_exists():
                self._mtl_poll_job = self.after(50, self._poll_mtl_queue)

    def on_batch_translate(self) -> None:
        """Open automated batch translation dialog."""
        if not self.current_doc or not self.current_doc.boxes:
            messagebox.showwarning("No Story Open", "Open a story bundle or text file first.")
            return
        BatchTranslateDialog(self)

    def on_copy_ai_prompt(self) -> None:
        """Export active story in CSIF format with AI system rules and delimiters (Part C.5)."""
        if not self.current_doc or not self.current_doc.boxes:
            self.show_toast("No story document loaded")
            return

        self._commit_widget_edit()
        lines: List[str] = []
        if getattr(self.mtl_config, "ai_prompt_include_header", True):
            hdr = getattr(self.mtl_config, "llm_system_prompt", "").strip()
            if hdr:
                lines.append(hdr)
                lines.append("")
            lines.append("=" * 60)
            lines.append("TRANSLATION INSTRUCTIONS & RULES:")
            lines.append("1. Maintain character personalities, tone, and visual novel style.")
            lines.append("2. Strictly preserve all CSIF headers: @@Speaker and @@_ (narration).")
            lines.append("3. Strictly preserve NGUI tags: [b], [i], [u], [s], [sub], [sup], [c]...[/c], [rub:ruby]base[/rub], [-]")
            lines.append("4. Strictly preserve tokens: {playername}, {0}, and line breaks.")
            lines.append("5. Output ONLY the translated story blocks in CSIF format.")
            lines.append("=" * 60)
            lines.append("")

        csif_body = serialize(self.current_doc, scope="all", include_metadata="auto")
        lines.append(csif_body)

        full_prompt = "\n".join(lines)
        self.safe_clipboard_set(full_prompt)
        box_count = len(self.current_doc.boxes)
        self.show_toast(f"📋 Copied AI prompt for {box_count} boxes (CSIF)")
        self.lbl_status.config(text=f"Copied AI prompt ({box_count} boxes in CSIF) to clipboard")

    def _show_paste_preview_and_apply(
        self,
        script_text: str,
        source_label: str = "Script Paste",
        confirm: bool = True,
    ) -> bool:
        """Unified method to parse, preview, and atomically apply script content to the open document (Phase 4 / Phase 5)."""
        if not self.current_doc or not self.current_doc.boxes:
            messagebox.showwarning("No Story Open", "Open a story bundle or text file first.")
            return False

        if not script_text or not script_text.strip():
            messagebox.showwarning("Empty Script", "The provided script text contains no readable content.")
            return False

        result = parse(script_text)

        # Route @@! metadata-only payloads to Box 0 (AGENTS.md Rule 20 D4)
        if not result.blocks and not result.metadata.is_empty():
            old_meta = self.current_doc.get_metadata()
            self.undo_journal.begin_batch("Paste Metadata (Box 0)")
            try:
                self.current_doc.set_metadata(
                    title=result.metadata.title,
                    subtitle=result.metadata.subtitle,
                    summary=result.metadata.summary,
                )
                self.undo_journal.record(
                    MetadataDelta(
                        file_path=str(self.current_file_path or ""),
                        old_title=old_meta.get("title", ""),
                        old_subtitle=old_meta.get("subtitle", ""),
                        old_summary=old_meta.get("summary", ""),
                        new_title=result.metadata.title or "",
                        new_subtitle=result.metadata.subtitle or "",
                        new_summary=result.metadata.summary or "",
                    )
                )
            finally:
                self.undo_journal.end_batch()
            self._mark_document_dirty(self.current_file_path)
            self._dirty_state_changed()
            self._update_views()
            self.show_toast("✓ Metadata applied to Box 0")
            return True

        if not result.blocks:
            messagebox.showwarning("No Dialogue Found", "No valid dialogue blocks found in script.")
            return False

        total_boxes = len(self.current_doc.boxes)
        if result.is_sparse:
            targets = []
            for blk in result.blocks:
                if blk.index is None or not (1 <= blk.index <= total_boxes):
                    raise IndexError(f"Sparse index #{blk.index} is out of range. Document has {total_boxes} boxes.")
                targets.append((blk.index - 1, blk))
            count = len(targets)
            start_idx = 0
        else:
            start_idx = max(0, self.current_box_idx)
            if start_idx >= total_boxes:
                start_idx = 0
            count = min(len(result.blocks), total_boxes - start_idx)
            if count <= 0:
                messagebox.showwarning("Target Full", "No remaining boxes available to paste into.")
                return False
            targets = [(start_idx + k, result.blocks[k]) for k in range(count)]

        apply_speakers = any(bool(b.speaker.strip()) for _, b in targets)
        apply_meta = not result.metadata.is_empty()

        if confirm:
            # Headless / mocked test compatibility check
            if messagebox.askyesno.__module__ != "tkinter.messagebox" or getattr(self, "_test_bypass_dialogs", False):
                preview_lines = []
                for i in range(min(len(targets), 3)):
                    t_idx, blk = targets[i]
                    target_box_num = t_idx + 1
                    snippet = " ".join(blk.text.splitlines())[:50]
                    preview_lines.append(f"  Box {target_box_num} [{blk.speaker or 'Narration'}]: {snippet}")
                if len(targets) > 3:
                    preview_lines.append(f"  ... and {len(targets) - 3} more boxes")
                if result.is_sparse:
                    target_desc = ", ".join(f"Box {t_idx + 1}" for t_idx, _ in targets)
                    prompt = (
                        f"Detected {len(result.blocks)} blocks ({result.format}).\n\n"
                        f"Target boxes: {target_desc} (sparse, of {total_boxes}).\n\n"
                        f"Preview:\n" + "\n".join(preview_lines) + "\n\n"
                        "Apply this script across these boxes?"
                    )
                else:
                    prompt = (
                        f"Detected {len(result.blocks)} blocks ({result.format}).\n\n"
                        f"Target range: Box {start_idx + 1} to Box {start_idx + count} (of {total_boxes}).\n\n"
                        f"Preview:\n" + "\n".join(preview_lines) + "\n\n"
                    )
                    if len(result.blocks) > count:
                        prompt += f"Note: {len(result.blocks) - count} excess blocks will be ignored.\n\n"
                    prompt += "Apply this script across these boxes?"
                if not messagebox.askyesno("Paste Across Boxes", prompt, parent=self):
                    return False
            else:
                dlg = ScriptPastePreviewDialog(self, result, start_idx if not result.is_sparse else 0, source_label=source_label)
                self.wait_window(dlg)
                if not dlg.confirmed:
                    return False
                apply_speakers = dlg.apply_speakers
                apply_meta = dlg.apply_metadata

        # Atomic commit via batch undo
        self._commit_widget_edit()
        locked_set = getattr(self, "_locked_boxes", set())
        skipped_locked = 0

        self.undo_journal.begin_batch(f"Apply Script ({source_label})")
        try:
            # Apply metadata if requested and present
            if apply_meta and not result.metadata.is_empty():
                old_meta = self.current_doc.get_metadata()
                self.current_doc.set_metadata(
                    title=result.metadata.title,
                    subtitle=result.metadata.subtitle,
                    summary=result.metadata.summary,
                )
                self.undo_journal.record(
                    MetadataDelta(
                        file_path=str(self.current_file_path or ""),
                        old_title=old_meta.get("title", ""),
                        old_subtitle=old_meta.get("subtitle", ""),
                        old_summary=old_meta.get("summary", ""),
                        new_title=result.metadata.title or "",
                        new_subtitle=result.metadata.subtitle or "",
                        new_summary=result.metadata.summary or "",
                    )
                )

            # Record box-level deltas in undo journal
            for b_idx, new_blk in targets:
                if b_idx in locked_set:
                    skipped_locked += 1
                    continue
                old_box = self.current_doc.boxes[b_idx]
                new_sp = new_blk.speaker if (apply_speakers and new_blk.speaker) else old_box.speaker
                old_uid = old_box.segs[0].record.uid if old_box.segs and old_box.segs[0].record else old_box.uid
                old_segs = [s.text for s in old_box.segs] if len(old_box.segs) > 1 else None
                new_segs = [new_blk.text] if len(old_box.segs) > 1 else None
                self.undo_journal.record(
                    BoxEditDelta(
                        box_index=b_idx,
                        old_speaker=old_box.speaker,
                        new_speaker=new_sp,
                        old_text=old_box.clean_text,
                        new_text=new_blk.text,
                        file_path=str(self.current_file_path or ""),
                        box_uid=old_uid,
                        old_seg_texts=old_segs,
                        new_seg_texts=new_segs,
                        source="paste_script",
                    )
                )

            applied_count = apply_to_document(
                self.current_doc,
                result,
                mode="replace",
                start_box_index=start_idx if not result.is_sparse else 0,
                apply_speakers=apply_speakers,
                apply_metadata=apply_meta,
                locked_indices=locked_set,
            )
            for b_idx, _ in targets:
                if b_idx not in locked_set:
                    self._modified_boxes.add(b_idx)
        finally:
            self.undo_journal.end_batch()

        self._mark_document_dirty(self.current_file_path)
        self._dirty_state_changed()
        self._update_views()
        msg = f"✓ Applied script across {applied_count} boxes"
        if skipped_locked > 0:
            msg += f" ({skipped_locked} locked boxes preserved)"
        self.show_toast(msg)
        self.lbl_status.config(text=f"Applied {source_label} across {applied_count} boxes.")
        return True

    def on_paste_cross_box(self, confirm: bool = True) -> None:
        """Apply multi-box translation from clipboard using CSIF codec with mode='replace' (Part C.3 / Phase 4)."""
        if not self.current_doc or not self.current_doc.boxes:
            messagebox.showwarning("No Story Open", "Open a story bundle or text file first.")
            return

        clip = self.safe_clipboard_get()
        if not clip.strip():
            messagebox.showwarning("Clipboard Empty", "Clipboard does not contain any readable text.")
            return

        self._show_paste_preview_and_apply(clip, source_label="Clipboard Paste", confirm=confirm)

    def on_import_script(self, file_path: Optional[Union[str, Path]] = None, confirm: bool = True) -> None:
        """Import script from a file (CSIF / Text) and apply it via preview dialog (Ctrl+Shift+I)."""
        if not self.current_doc or not self.current_doc.boxes:
            messagebox.showwarning("No Story Open", "Open a story bundle or text file first.")
            return

        if not file_path:
            file_types = [
                ("CSIF / Text Files", "*.txt;*.csif;*.md"),
                ("Text Files (*.txt)", "*.txt"),
                ("CSIF Files (*.csif)", "*.csif"),
                ("All Files (*.*)", "*.*"),
            ]
            selected = filedialog.askopenfilename(
                title="Import Script (CSIF / Text)",
                filetypes=file_types,
                parent=self,
            )
            if not selected:
                return
            target_file = Path(selected)
        else:
            target_file = Path(file_path)

        if not target_file.is_file():
            messagebox.showerror("File Not Found", f"Cannot find import file:\n{target_file}", parent=self)
            return

        try:
            decoded = read_text_file_strictly(target_file)
            content = decoded.text
        except UnicodeDecodeError as exc:
            self.logger.exception("Failed to decode import file:", exc)
            messagebox.showerror("Import Failed", f"Could not decode script file:\n{exc}", parent=self)
            return
        except Exception as exc:
            self.logger.exception("Failed to read import file:", exc)
            messagebox.showerror("Import Failed", f"Could not read script file:\n{exc}", parent=self)
            return

        self._show_paste_preview_and_apply(content, source_label=f"Import ({target_file.name})", confirm=confirm)

    def _get_xuat_index_roots(self) -> List[Path]:
        """Collect candidate roots for strict BepInEx\\Translation\\en\\Text XUAT indexing."""
        roots: List[Path] = []
        if getattr(self, "xuat_search_roots", None):
            roots.extend(self.xuat_search_roots)
        elif getattr(self, "project_folder", None):
            roots.append(self.project_folder)
        return resolve_xuat_text_roots(roots)

    def _refresh_xuat_index_async(self) -> None:
        """Start background XUAT dictionary indexing and poll on the Tk main thread (Rule 15)."""
        if getattr(self, "_xuat_index_cancel", None) is not None:
            try:
                self._xuat_index_cancel.set()
            except Exception:
                pass
        strict_roots = self._get_xuat_index_roots()
        if not strict_roots:
            self.xuat_index = None
            self.xuat_entries = None
            self._xuat_index_cancel = None
            return
        self._xuat_index_seq += 1
        seq = self._xuat_index_seq
        cancel_ev = threading.Event()
        self._xuat_index_cancel = cancel_ev
        build_xuat_index_async(
            strict_roots,
            out_queue=self._xuat_index_queue,
            metadata=seq,
            cancel_event=cancel_ev,
        )
        if self._xuat_index_poll_id is None and self.winfo_exists():
            self._xuat_index_poll_id = self.after(50, self._poll_xuat_index_queue)

    def _poll_xuat_index_queue(self) -> None:
        """Poll background XUAT index builds strictly while a build is in flight (BUG-27)."""
        self._xuat_index_poll_id = None
        if not self.winfo_exists() or getattr(self, "_destroyed", False):
            return
        latest_applied = False
        try:
            while True:
                kind, seq, payload = self._xuat_index_queue.get_nowait()
                if seq != self._xuat_index_seq:
                    continue
                if kind == "xuat_index_ready":
                    self.xuat_index = payload
                    self.xuat_entries = payload
                    latest_applied = True
                elif kind == "xuat_index_error":
                    self.logger.warning("XUAT Index", f"Background XUAT index failed: {payload}")
                    latest_applied = True
        except queue.Empty:
            pass

        if not latest_applied and self.winfo_exists() and not getattr(self, "_destroyed", False):
            self._xuat_index_poll_id = self.after(50, self._poll_xuat_index_queue)

    def _get_or_build_xuat_index(self, force_rebuild: bool = False) -> XuatIndex:
        """Return unified XuatIndex (D11), building synchronously if not yet cached."""
        strict_roots = self._get_xuat_index_roots()
        if not force_rebuild and isinstance(getattr(self, "xuat_index", None), XuatIndex):
            if self.xuat_index.roots == strict_roots:
                return self.xuat_index
        idx = build_xuat_index(strict_roots)
        self.xuat_index = idx
        self.xuat_entries = idx
        return idx

    def on_import_from_xuat(self, xuat_index: Optional[XuatIndex] = None) -> Optional["ImportFromXUATDialog"]:
        """Open separate floating Import from XUAT resolver; auto-closes MTL drawer (FEAT-14 / U-B34)."""
        if not self.current_doc or not self.current_doc.boxes:
            messagebox.showwarning("No Story Open", "Open a story bundle or text file first.", parent=self)
            return None

        # Auto-close docked MTL drawer when opening Import from XUAT
        if getattr(self, "_side_drawer_visible", False) and getattr(self, "_side_drawer_tab", "") == "mtl":
            self._close_side_drawer()

        idx = xuat_index if xuat_index is not None else self._get_or_build_xuat_index()
        existing = getattr(self, "_import_xuat_dialog", None)
        if existing is not None:
            try:
                if existing.winfo_exists():
                    existing.lift()
                    existing.focus_force()
                    return existing
            except Exception:
                pass

        dlg = ImportFromXUATDialog(self, idx)
        self._import_xuat_dialog = dlg
        return dlg

    def on_export_script(self, file_path: Optional[Union[str, Path]] = None) -> Optional[Path]:
        """Export active story in CSIF format to a file (Ctrl+Shift+E)."""
        if not self.current_doc or not self.current_doc.boxes:
            messagebox.showwarning("No Story Open", "Open a story bundle or text file first.")
            return None

        if not file_path:
            init_name = f"{self.current_file_path.stem}.csif.txt" if self.current_file_path else "story_export.csif.txt"
            file_types = [
                ("CSIF Text File (*.txt)", "*.txt"),
                ("CSIF Script (*.csif)", "*.csif"),
                ("All Files (*.*)", "*.*"),
            ]
            selected = filedialog.asksaveasfilename(
                title="Export Script (CSIF)",
                defaultextension=".txt",
                initialfile=init_name,
                filetypes=file_types,
                parent=self,
            )
            if not selected:
                return None
            target_path = Path(selected)
        else:
            target_path = Path(file_path)

        self._commit_widget_edit()
        try:
            csif_text = serialize(self.current_doc, scope="all", include_metadata="auto")
            target_path.parent.mkdir(parents=True, exist_ok=True)
            write_atomic_encoded(target_path, csif_text, encoding="utf-8", newline="\n")
        except Exception as exc:
            self.logger.exception("Failed to export script:", exc)
            messagebox.showerror("Export Failed", f"Could not write export file:\n{exc}", parent=self)
            return None

        box_count = len(self.current_doc.boxes)
        self.show_toast(f"✓ Exported {box_count} boxes to {target_path.name}")
        self.lbl_status.config(text=f"Exported script to {target_path}")
        return target_path

    # Universal alias for cross-box script pasting
    on_apply_translation_clipboard = on_paste_cross_box

    def on_clear_dialogue_skeleton(self) -> None:
        """Clear all dialogue text across all boxes, keeping speaker names and skeleton intact."""
        if not self.current_doc or not self.current_doc.boxes:
            self.show_toast("No story document loaded")
            return
        total = len(self.current_doc.boxes)
        ans = messagebox.askyesno(
            "Clear Dialogue Skeleton",
            f"Clear all dialogue text across all {total} boxes?\n\n"
            "This preserves speaker names, tags, and box timing while resetting dialogue to blank for a fresh translation pass.\n\n"
            "This operation can be undone via Ctrl+Z."
        )
        if not ans:
            return

        cleared_count = 0
        preserved_count = 0
        self.undo_journal.begin_batch("Clear Dialogue Skeleton")
        try:
            for i, box in enumerate(self.current_doc.boxes):
                if self.is_box_locked(i):
                    preserved_count += 1
                    continue
                if box.clean_text:
                    old_sp = box.speaker
                    old_tx = box.clean_text
                    box_uid = box.uid
                    try:
                        self.current_doc.inject_box(i, old_sp, "")
                    except Exception as e:
                        self.logger.exception(f"Failed to clear box {i}:", e)
                        continue

                    self.undo_journal.record(
                        BoxEditDelta(
                            box_index=i,
                            old_speaker=old_sp,
                            new_speaker=old_sp,
                            old_text=old_tx,
                            new_text="",
                            file_path=str(self.current_file_path) if self.current_file_path else "",
                            box_uid=box_uid,
                            source="clear",
                        )
                    )
                    self._modified_boxes.add(i)
                    cleared_count += 1
        finally:
            self.undo_journal.end_batch()

        if cleared_count > 0:
            self._mark_document_dirty(self.current_file_path)
            self._dirty_state_changed()
            self._update_views()

        msg = f"Cleared dialogue skeleton for {cleared_count} boxes"
        if preserved_count > 0:
            msg += f" (preserved {preserved_count} locked)"
        self.show_toast(f"✓ {msg}")
        self.lbl_status.config(text=f"{msg}.")

    def on_register_unity3d_association(self) -> None:
        """Register or verify .unity3d file association for current Windows user (#8)."""
        bat_path = SCRIPT_DIR / "misora.bat"
        if not bat_path.exists():
            messagebox.showerror("Association Error", f"Cannot find {bat_path}")
            return

        cmd_str = f'"{bat_path}" "%1"'
        try:
            already_registered = False
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.unity3d") as key:
                    val, _ = winreg.QueryValueEx(key, "")
                    if val == "Misora.Unity3dBundle":
                        already_registered = True
            except OSError:
                pass

            if already_registered:
                ans = messagebox.askyesno(
                    ".unity3d File Association",
                    ".unity3d files are currently associated with Misora.\n\nDo you want to unregister (remove) this association?"
                )
                if ans:
                    try:
                        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Misora.Unity3dBundle\shell\open\command")
                        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Misora.Unity3dBundle\shell\open")
                        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Misora.Unity3dBundle\shell")
                        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Misora.Unity3dBundle")
                        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.unity3d")
                        self.show_toast("✓ Removed .unity3d file association")
                        messagebox.showinfo("Success", ".unity3d association removed successfully.")
                    except Exception as exc:
                        self.logger.exception("Failed to remove .unity3d association:", exc)
                        messagebox.showerror("Error", f"Failed to remove association:\n{exc}")
                return

            ans = messagebox.askyesno(
                "Register .unity3d File Association",
                f"Associate .unity3d story files with Misora for the current user?\n\nTarget launcher:\n{bat_path}\n\nThis does not require Administrator privileges."
            )
            if not ans:
                return

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.unity3d") as k1:
                winreg.SetValueEx(k1, "", 0, winreg.REG_SZ, "Misora.Unity3dBundle")

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Misora.Unity3dBundle") as k2:
                winreg.SetValueEx(k2, "", 0, winreg.REG_SZ, "Unity3D Story Bundle (Misora)")

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Misora.Unity3dBundle\shell\open\command") as k3:
                winreg.SetValueEx(k3, "", 0, winreg.REG_SZ, cmd_str)

            try:
                ctypes.windll.shell32.SHChangeNotify(0x08000000, 0, 0, 0)
            except Exception:
                pass

            self.logger.info("Config", "Registered .unity3d file association for HKCU")
            self.show_toast("✓ Registered .unity3d file association")
            messagebox.showinfo("Success", ".unity3d story bundles are now associated with Misora!")
        except Exception as exc:
            self.logger.exception("Failed to register .unity3d association:", exc)
            messagebox.showerror("Registration Failed", f"Could not write registry keys:\n{exc}")

    def on_about(self) -> None:
        """Show application information dialog."""
        about_text = (
            "Misora: Unity3D Revision Tool & Story Editor\n"
            f"Version {__version__}\n\n"
            "A specialized GUI text editor for Princess Connect! Re:Dive\n"
            "Unity3D story bundles (.unity3d) and XUAT translation files.\n\n"
            "MIT License — Created for the Priconne Modding Community."
        )
        messagebox.showinfo("About Misora", about_text)


# =============================================================================
# Script Paste / Import Preview Dialog (Phase 4)
# =============================================================================
class ScriptPastePreviewDialog(tk.Toplevel):
    """Interactive preview and confirmation dialog for script paste and import operations (Part C.5 / Phase 4)."""

    def __init__(
        self,
        parent: "MisoraApp",
        parsed_result,
        start_idx: int,
        source_label: str = "Script Paste",
    ):
        super().__init__(parent)
        self.app = parent
        self.result = parsed_result
        self.start_idx = start_idx
        self.source_label = source_label
        self.confirmed = False

        self.title("Paste / Import Script Preview")
        self.geometry("860x640")
        self.minsize(720, 480)
        self.transient(parent)
        self.grab_set()

        t = self.app.theme
        self.configure(bg=t["bg_panel"])
        apply_window_icon(self)

        fg_panel = best_contrast_fg(t["bg_panel"])
        fg_editor = best_contrast_fg(t["bg_editor"])

        total_doc_boxes = len(self.app.current_doc.boxes) if self.app.current_doc else 0
        blocks = self.result.blocks
        if self.result.is_sparse:
            self.count = len(blocks)
            has_speakers = any(bool(b.speaker.strip()) for b in blocks)
        else:
            self.count = min(len(blocks), max(0, total_doc_boxes - start_idx))
            has_speakers = any(bool(b.speaker.strip()) for b in blocks[:self.count])
        has_meta = not self.result.metadata.is_empty()

        self.var_apply_speakers = tk.BooleanVar(master=self, value=has_speakers)
        self.var_apply_metadata = tk.BooleanVar(master=self, value=has_meta)

        self.apply_speakers = has_speakers
        self.apply_metadata = has_meta

        self._build_ui(t, fg_panel, fg_editor, total_doc_boxes, blocks, has_meta)

        # Center on parent window
        self.update_idletasks()
        try:
            px = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
            py = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
            self.geometry(f"+{max(0, px)}+{max(0, py)}")
        except Exception:
            pass

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.bind("<Escape>", lambda _e=None: self.on_cancel())

    def _build_ui(self, t: dict, fg_panel: str, fg_editor: str, total_doc_boxes: int, blocks: list, has_meta: bool) -> None:
        container = tk.Frame(self, bg=t["bg_panel"], padx=14, pady=10)
        container.pack(fill="both", expand=True)

        # 1. Header Banner & Info
        hdr_frame = tk.Frame(container, bg=t["bg_panel"])
        hdr_frame.pack(fill="x", pady=(0, 8))

        lbl_title = tk.Label(
            hdr_frame,
            text=f"Script Preview — {self.source_label}",
            font=("Segoe UI", 12, "bold"),
            bg=t["bg_panel"],
            fg=t["misora_pink"],
        )
        lbl_title.pack(anchor="w")

        if self.result.is_sparse:
            sparse_box_names = ", ".join(f"Box {b.index}" for b in blocks if b.index is not None)
            info_lines = [
                f"Format: {self.result.format.upper()} (Sparse)  |  Detected: {len(blocks)} blocks  |  Targets: {sparse_box_names} (of {total_doc_boxes})"
            ]
        else:
            info_lines = [
                f"Format: {self.result.format.upper()}  |  Detected: {len(blocks)} blocks  |  Target: Box {self.start_idx + 1} to {self.start_idx + self.count} (of {total_doc_boxes})"
            ]
            if len(blocks) > self.count:
                excess = len(blocks) - self.count
                info_lines.append(f"⚠ Notice: {excess} excess block(s) will be skipped as they exceed total boxes.")
        if has_meta:
            m = self.result.metadata
            m_parts = []
            if m.title:
                m_parts.append(f"Title: '{m.title}'")
            if m.subtitle:
                m_parts.append(f"Subtitle: '{m.subtitle}'")
            if m_parts:
                info_lines.append("Metadata detected: " + ", ".join(m_parts))

        lbl_info = tk.Label(
            hdr_frame,
            text="\n".join(info_lines),
            font=("Segoe UI", 9),
            bg=t["bg_panel"],
            fg=fg_panel,
            justify="left",
        )
        lbl_info.pack(anchor="w", pady=(2, 0))

        # 2. Options Checkboxes
        opts_frame = tk.Frame(container, bg=t["bg_panel"])
        opts_frame.pack(fill="x", pady=(4, 6))

        cb_speakers = ttk.Checkbutton(
            opts_frame,
            text="Apply speaker names from script",
            variable=self.var_apply_speakers,
            command=self._populate_tree,
        )
        cb_speakers.pack(side="left", padx=(0, 16))

        if has_meta:
            cb_meta = ttk.Checkbutton(
                opts_frame,
                text="Apply metadata (title / subtitle / summary) to Box 0",
                variable=self.var_apply_metadata,
            )
            cb_meta.pack(side="left")

        # 3. Comparison Treeview
        tree_frame = tk.Frame(container, bg=t["bg_editor"], bd=1, relief="solid")
        tree_frame.pack(fill="both", expand=True, pady=(2, 8))

        columns = ("box", "cur_spk", "new_spk", "cur_text", "new_text")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("box", text="Box #")
        self.tree.heading("cur_spk", text="Current Speaker")
        self.tree.heading("new_spk", text="Incoming Speaker")
        self.tree.heading("cur_text", text="Current Text (Preview)")
        self.tree.heading("new_text", text="Incoming Text (Preview)")

        self.tree.column("box", width=70, minwidth=50, anchor="center")
        self.tree.column("cur_spk", width=120, minwidth=80, anchor="w")
        self.tree.column("new_spk", width=130, minwidth=80, anchor="w")
        self.tree.column("cur_text", width=250, minwidth=140, anchor="w")
        self.tree.column("new_text", width=250, minwidth=140, anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._populate_tree()

        # 4. Action Buttons
        btn_row = tk.Frame(container, bg=t["bg_panel"])
        btn_row.pack(fill="x", pady=(4, 0))

        btn_apply = tk.Button(
            btn_row,
            text="Apply Changes",
            bg=t["accent_blue"],
            fg="#ffffff",
            activebackground=t["accent_blue"],
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=16,
            pady=4,
            relief="raised",
            cursor="hand2",
            command=self.on_apply,
        )
        btn_apply.pack(side="right", padx=(8, 0))

        btn_cancel = tk.Button(
            btn_row,
            text="Cancel",
            bg=t["bg_editor"],
            fg=fg_editor,
            activebackground=t["bg_editor"],
            activeforeground=fg_editor,
            font=("Segoe UI", 9),
            padx=14,
            pady=4,
            relief="raised",
            cursor="hand2",
            command=self.on_cancel,
        )
        btn_cancel.pack(side="right")

    def _populate_tree(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        blocks = self.result.blocks
        apply_speakers = self.var_apply_speakers.get()

        if self.result.is_sparse:
            for new_blk in blocks:
                if new_blk.index is None:
                    continue
                b_idx = new_blk.index - 1
                if not (0 <= b_idx < len(self.app.current_doc.boxes)):
                    continue
                old_box = self.app.current_doc.boxes[b_idx]
                cur_spk = old_box.speaker or "(narration)"
                if apply_speakers:
                    new_spk = new_blk.speaker if new_blk.speaker else "(narration)"
                else:
                    new_spk = f"{cur_spk} (keep)"

                cur_txt = " ".join(old_box.clean_text.splitlines())[:80]
                new_txt = " ".join(new_blk.text.splitlines())[:80]
                self.tree.insert("", "end", values=(f"Box {new_blk.index}", cur_spk, new_spk, cur_txt, new_txt))
        else:
            for k in range(self.count):
                b_idx = self.start_idx + k
                old_box = self.app.current_doc.boxes[b_idx]
                new_blk = blocks[k]

                cur_spk = old_box.speaker or "(narration)"
                if apply_speakers:
                    new_spk = new_blk.speaker if new_blk.speaker else "(narration)"
                else:
                    new_spk = f"{cur_spk} (keep)"

                cur_txt = " ".join(old_box.clean_text.splitlines())[:80]
                new_txt = " ".join(new_blk.text.splitlines())[:80]

                self.tree.insert("", "end", values=(f"Box {b_idx + 1}", cur_spk, new_spk, cur_txt, new_txt))

    def on_apply(self) -> None:
        self.apply_speakers = self.var_apply_speakers.get()
        self.apply_metadata = self.var_apply_metadata.get()
        self.confirmed = True
        safe_grab_release(self)
        self.destroy()

    def on_cancel(self) -> None:
        self.confirmed = False
        safe_grab_release(self)
        self.destroy()


# =============================================================================
# Floating Import from XUAT Resolver Dialog (S22 / FEAT-14 / U-B34)
# =============================================================================
class ImportFromXUATDialog(tk.Toplevel):
    """Separate floating resolver pairing Story boxes (left) with XUAT matches (right).

    Both sides are strictly read-only (state='disabled') with fixed 3 lines x 50 digit-widths
    (via S17 _measure_dialogue_metrics) and zero per-box Scrollbar widgets.
    """

    def __init__(self, parent: "MisoraApp", xuat_index: XuatIndex):
        super().__init__(parent)
        self.app = parent
        self.xuat_index = xuat_index
        self._rows: List[Dict[str, Any]] = []
        self._focused_box_widget: Optional[tk.Text] = None
        self._active_filter: str = "all"
        self._speaker_matches: Dict[int, str] = {}
        self._filter_buttons: Dict[str, ttk.Button] = {}
        self._canvas_win_id: Optional[int] = None

        self.title("Import from XUAT (Read-Only Paired Resolver)")
        self.geometry("980x680")
        self.minsize(820, 520)
        self.transient(parent)

        t = self.app.theme
        self.configure(bg=t["bg_panel"])
        apply_window_icon(self)

        self.var_translate_speakers = tk.BooleanVar(master=self, value=False)
        self._build_ui()
        self._populate_rows()

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.bind("<Escape>", lambda _e=None: self._on_close())

    def _build_ui(self) -> None:
        t = self.app.theme
        fg_panel = best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff")

        top = tk.Frame(self, bg=t["bg_panel"], padx=12, pady=8)
        top.pack(fill="x")

        title_row = tk.Frame(top, bg=t["bg_panel"])
        title_row.pack(fill="x")

        tk.Label(
            title_row,
            text="Import from XUAT Dictionary",
            font=("Segoe UI", 12, "bold"),
            bg=t["bg_panel"],
            fg=t["misora_pink"],
        ).pack(side="left")

        ttk.Button(
            title_row,
            text="↻ Reload XUAT Index",
            style="Small.TButton",
            command=self._on_reload_index,
        ).pack(side="right")

        self.lbl_summary = tk.Label(
            top,
            text="Dialogue: 0 matched | Speakers: 0 matched",
            font=("Segoe UI", 9),
            bg=t["bg_panel"],
            fg=fg_panel,
            anchor="w",
        )
        self.lbl_summary.pack(fill="x", pady=(4, 4))

        ctrl_row = tk.Frame(top, bg=t["bg_panel"])
        ctrl_row.pack(fill="x", pady=(2, 0))

        for f_key, f_label in (
            ("all", "All"),
            ("duplicates", "Duplicates"),
            ("missing", "Missing"),
            ("matched", "Matched"),
        ):
            btn = ttk.Button(
                ctrl_row,
                text=f_label,
                style="Pink.TButton" if f_key == "all" else "TButton",
                command=lambda k=f_key: self._set_filter(k),
            )
            btn.pack(side="left", padx=(0, 4))
            self._filter_buttons[f_key] = btn

        cb_spk = tk.Checkbutton(
            ctrl_row,
            text="Also translate speaker names",
            variable=self.var_translate_speakers,
            bg=t["bg_panel"],
            fg=fg_panel,
            selectcolor=t["bg_dark"],
            activebackground=t["bg_panel"],
            activeforeground=fg_panel,
        )
        cb_spk.pack(side="right")

        # Outer scrollable list (single outer vertical scrollbar)
        list_wrap = tk.Frame(self, bg=t["bg_dark"], bd=1, relief="solid")
        list_wrap.pack(fill="both", expand=True, padx=12, pady=6)

        self.list_canvas = tk.Canvas(list_wrap, bg=t["bg_dark"], highlightthickness=0)
        self.outer_vsb = ttk.Scrollbar(list_wrap, orient="vertical", command=self.list_canvas.yview)
        self.list_canvas.configure(yscrollcommand=self.outer_vsb.set)

        self.outer_vsb.pack(side="right", fill="y")
        self.list_canvas.pack(side="left", fill="both", expand=True)

        self.rows_frame = tk.Frame(self.list_canvas, bg=t["bg_dark"])
        self._canvas_win_id = self.list_canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")

        self.rows_frame.bind("<Configure>", self._on_rows_configure)
        self.list_canvas.bind("<Configure>", self._on_canvas_configure)
        self.list_canvas.bind("<MouseWheel>", self._on_outer_mousewheel)
        self.rows_frame.bind("<MouseWheel>", self._on_outer_mousewheel)

        # Bottom action bar
        btn_bar = tk.Frame(self, bg=t["bg_panel"], padx=12, pady=8)
        btn_bar.pack(fill="x", side="bottom")

        ttk.Button(btn_bar, text="Cancel", style="TButton", command=self._on_close).pack(side="right", padx=4)
        ttk.Button(btn_bar, text="Apply Import", style="Pink.TButton", command=self._on_apply_import).pack(
            side="right", padx=4
        )

    def _on_rows_configure(self, _event: Optional[tk.Event] = None) -> None:
        if self.list_canvas.winfo_exists():
            self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        if self.list_canvas.winfo_exists() and self._canvas_win_id is not None:
            self.list_canvas.itemconfig(self._canvas_win_id, width=event.width)

    def _on_outer_mousewheel(self, event: tk.Event) -> str:
        if self.list_canvas.winfo_exists() and getattr(event, "delta", 0):
            self.list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def _on_reload_index(self) -> None:
        self.xuat_index = self.app._get_or_build_xuat_index(force_rebuild=True)
        self._populate_rows()

    def _get_immutable_jp_key(self, box_idx: int, box: Box) -> str:
        """Resolve immutable JP source key by box_uid (BUG-25 / DEP-7)."""
        b_uid = _get_box_uid(box)
        orig_map = getattr(self.app, "_original_jp_by_uid", {})
        if b_uid is not None and b_uid in orig_map and orig_map[b_uid]:
            return orig_map[b_uid]
        if hasattr(self.app, "sync_manager") and self.app.sync_manager is not None:
            jp = self.app.sync_manager.get_jp_key(b_uid)
            if jp:
                return jp
        return box.clean_text

    def _populate_rows(self) -> None:
        for child in self.rows_frame.winfo_children():
            child.destroy()
        self._rows.clear()
        self._speaker_matches.clear()
        self._focused_box_widget = None

        doc = self.app.current_doc
        if not doc or not doc.boxes:
            return

        t = self.app.theme
        fg_panel = best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff")
        fg_editor = best_contrast_fg(t["bg_editor"], t["fg_text"], "#ffffff")
        fg_muted = t["fg_muted"]

        measure_font = self.app._get_dialogue_measure_font()
        safe_w = self.app._measure_dialogue_metrics("1234567890" * 5)["safe_w"]
        line_h = max(14, int(measure_font.metrics("linespace")))
        box_px_w = safe_w + 10
        box_px_h = line_h * 3 + 8

        orig_map = getattr(self.app, "_original_jp_by_uid", {})
        stats = analyze_story_matches(doc, orig_map, self.xuat_index)
        self.lbl_summary.config(
            text=(
                f"Dialogue: {stats['dialogue_matched']}/{stats['dialogue_total']} matched "
                f"({stats['dialogue_duplicates']} duplicates, {stats['dialogue_missing']} missing)  |  "
                f"Speakers: {stats['speaker_matched']}/{stats['speaker_total']} matched "
                f"({stats['speaker_missing']} missing)  |  "
                f"Files indexed: {len(self.xuat_index.files_indexed)}"
            )
        )

        # Update filter chip labels
        chip_counts = {
            "all": stats["dialogue_total"],
            "duplicates": stats["dialogue_duplicates"],
            "missing": stats["dialogue_missing"],
            "matched": stats["dialogue_matched"],
        }
        chip_names = {"all": "All", "duplicates": "Duplicates", "missing": "Missing", "matched": "Matched"}
        for k, btn in self._filter_buttons.items():
            btn.config(text=f"{chip_names[k]} ({chip_counts[k]})")

        global_overrides = getattr(self.app, "_xuat_global_choice_overrides", {})

        for idx, box in enumerate(doc.boxes):
            b_uid = _get_box_uid(box)
            jp_key = self._get_immutable_jp_key(idx, box)
            norm_k = normalize_xuat_key(jp_key, strip_ngui=True)
            lookup = self.xuat_index.lookup_candidates(jp_key)
            is_locked = self.app.is_box_locked(idx)

            if box.speaker:
                sp_hit = self.xuat_index.lookup_translation(box.speaker)
                if sp_hit is not None:
                    self._speaker_matches[idx] = sp_hit

            # Determine default candidate index (respecting in-memory global override if any)
            cand_idx = 0
            if lookup.candidates and norm_k in global_overrides:
                pref_val = global_overrides[norm_k]
                for ci, cand in enumerate(lookup.candidates):
                    if cand.value == pref_val:
                        cand_idx = ci
                        break

            row_bg = t["bg_dark"] if is_locked else t["bg_panel"]
            card = tk.Frame(
                self.rows_frame,
                bg=row_bg,
                bd=1,
                relief="solid",
                highlightbackground=t["border"],
                highlightthickness=1,
                padx=8,
                pady=6,
            )
            card.pack(fill="x", padx=6, pady=4)
            card.bind("<MouseWheel>", self._on_outer_mousewheel)

            # Row Header
            hdr = tk.Frame(card, bg=row_bg)
            hdr.pack(fill="x", pady=(0, 4))
            hdr.bind("<MouseWheel>", self._on_outer_mousewheel)

            spk_label = box.speaker if box.speaker else "(Narration)"
            tk.Label(
                hdr,
                text=f"Box #{idx + 1:03d} — {spk_label}",
                font=("Segoe UI", 9, "bold"),
                bg=row_bg,
                fg=fg_muted if is_locked else t["misora_pink"],
            ).pack(side="left")

            if is_locked:
                tk.Label(
                    hdr,
                    text="🔒 Locked (Auto-Skip)",
                    font=("Segoe UI", 8, "bold"),
                    bg=row_bg,
                    fg=fg_muted,
                ).pack(side="left", padx=(8, 4))

            var_skip = tk.BooleanVar(master=self, value=is_locked)
            cb_skip = tk.Checkbutton(
                hdr,
                text="Skip",
                variable=var_skip,
                state="disabled" if is_locked else "normal",
                bg=row_bg,
                fg=fg_muted if is_locked else fg_panel,
                disabledforeground=fg_muted,
                selectcolor=t["bg_dark"],
                activebackground=row_bg,
                activeforeground=fg_panel,
            )
            cb_skip.pack(side="right")

            # Provenance + duplicate controls
            prov_text = lookup.candidates[cand_idx].provenance if lookup.candidates else "No XUAT match"
            lbl_provenance = tk.Label(
                hdr,
                text=prov_text,
                font=("Consolas", 8),
                bg=row_bg,
                fg=fg_muted,
            )
            lbl_provenance.pack(side="right", padx=(6, 8))

            lbl_dup_counter = tk.Label(hdr, text="", font=("Segoe UI", 8, "bold"), bg=row_bg, fg=t["accent_blue"])
            var_scope = tk.StringVar(master=self, value="This Box")
            if lookup.status == "duplicate":
                scope_cmb = ttk.Combobox(
                    hdr,
                    textvariable=var_scope,
                    values=("This Box", "This Story", "Global"),
                    state="readonly",
                    width=10,
                )
                scope_cmb.pack(side="right", padx=(4, 4))
                scope_cmb.bind(
                    "<<ComboboxSelected>>",
                    lambda _e, r_idx=idx: self._apply_conflict_scope(r_idx),
                )

                btn_next = ttk.Button(hdr, text="▶", width=2, style="Small.TButton", command=lambda r_idx=idx: self._step_candidate(r_idx, 1))
                btn_next.pack(side="right", padx=(1, 2))
                lbl_dup_counter.config(text=f"{cand_idx + 1}/{len(lookup.candidates)}")
                lbl_dup_counter.pack(side="right", padx=2)
                btn_prev = ttk.Button(hdr, text="◀", width=2, style="Small.TButton", command=lambda r_idx=idx: self._step_candidate(r_idx, -1))
                btn_prev.pack(side="right", padx=(2, 1))

            # Paired Left (Story) & Right (XUAT) 3x50 read-only boxes
            pair_frame = tk.Frame(card, bg=row_bg)
            pair_frame.pack(fill="x")
            pair_frame.bind("<MouseWheel>", self._on_outer_mousewheel)

            left_col = tk.Frame(pair_frame, bg=row_bg)
            left_col.pack(side="left", padx=(0, 8))
            left_hdr = tk.Frame(left_col, bg=row_bg)
            left_hdr.pack(fill="x")
            tk.Label(left_hdr, text="Story (JP / Current)", font=("Segoe UI", 8), bg=row_bg, fg=fg_muted).pack(side="left")
            left_m = self.app._measure_dialogue_metrics(jp_key)
            left_ov_badge = ("▼" if left_m["has_line_overflow"] else "") + ("▶" if left_m["has_width_overflow"] else "")
            lbl_left_overflow = tk.Label(left_hdr, text=left_ov_badge, font=("Segoe UI", 8, "bold"), bg=row_bg, fg=t["accent_yellow"])
            lbl_left_overflow.pack(side="right")

            left_wrap = tk.Frame(left_col, width=box_px_w, height=box_px_h, bg=t["bg_editor"], bd=1, relief="solid")
            left_wrap.pack_propagate(False)
            left_wrap.pack()

            txt_left = tk.Text(
                left_wrap,
                font=measure_font,
                height=3,
                width=50,
                wrap="none",
                bg=t["bg_dark"] if is_locked else t["bg_editor"],
                fg=fg_muted if is_locked else fg_editor,
                bd=0,
                highlightthickness=0,
                padx=3,
                pady=2,
            )
            txt_left.insert("1.0", jp_key)
            txt_left.config(state="disabled")
            txt_left.pack(fill="both", expand=True)

            right_col = tk.Frame(pair_frame, bg=row_bg)
            right_col.pack(side="left")
            right_hdr = tk.Frame(right_col, bg=row_bg)
            right_hdr.pack(fill="x")
            tk.Label(right_hdr, text="XUAT Match", font=("Segoe UI", 8), bg=row_bg, fg=fg_muted).pack(side="left")

            right_text = lookup.candidates[cand_idx].value if lookup.candidates else ""
            right_m = self.app._measure_dialogue_metrics(right_text)
            right_ov_badge = ("▼" if right_m["has_line_overflow"] else "") + ("▶" if right_m["has_width_overflow"] else "")
            lbl_right_overflow = tk.Label(right_hdr, text=right_ov_badge, font=("Segoe UI", 8, "bold"), bg=row_bg, fg=t["accent_yellow"])
            lbl_right_overflow.pack(side="right")

            right_wrap = tk.Frame(right_col, width=box_px_w, height=box_px_h, bg=t["bg_editor"], bd=1, relief="solid")
            right_wrap.pack_propagate(False)
            right_wrap.pack()

            txt_right = tk.Text(
                right_wrap,
                font=measure_font,
                height=3,
                width=50,
                wrap="none",
                bg=t["bg_dark"] if is_locked else t["bg_editor"],
                fg=fg_muted if is_locked else fg_editor,
                bd=0,
                highlightthickness=0,
                padx=3,
                pady=2,
            )
            txt_right.insert("1.0", right_text)
            txt_right.config(state="disabled")
            txt_right.pack(fill="both", expand=True)

            self._bind_paired_box_events(txt_left, left_m["has_line_overflow"], left_m["has_width_overflow"])
            self._bind_paired_box_events(txt_right, right_m["has_line_overflow"], right_m["has_width_overflow"])

            self._rows.append(
                {
                    "box_idx": idx,
                    "box_uid": b_uid,
                    "norm_key": norm_k,
                    "status": lookup.status,
                    "candidates": lookup.candidates,
                    "cand_idx": cand_idx,
                    "is_locked": is_locked,
                    "var_skip": var_skip,
                    "cb_skip": cb_skip,
                    "var_scope": var_scope,
                    "frame": card,
                    "left_wrap": left_wrap,
                    "right_wrap": right_wrap,
                    "txt_left": txt_left,
                    "txt_right": txt_right,
                    "lbl_left_overflow": lbl_left_overflow,
                    "lbl_right_overflow": lbl_right_overflow,
                    "lbl_provenance": lbl_provenance,
                    "lbl_dup_counter": lbl_dup_counter,
                }
            )

        self._set_filter(self._active_filter)

    def _bind_paired_box_events(self, txt: tk.Text, has_v: bool, has_h: bool) -> None:
        """Focus-gated inner vertical wheel & horizontal Shift+Wheel/drag; outer scroll otherwise."""
        def _on_press(event: tk.Event) -> None:
            self._focused_box_widget = txt
            try:
                txt.focus_set()
                if has_h:
                    txt.scan_mark(event.x, event.y)
            except Exception:
                pass

        def _on_drag(event: tk.Event) -> None:
            if self._focused_box_widget is txt and has_h:
                try:
                    txt.scan_dragto(event.x, event.y, gain=1)
                except Exception:
                    pass

        def _on_focus_out(_event: tk.Event) -> None:
            if self._focused_box_widget is txt:
                self._focused_box_widget = None

        def _on_wheel(event: tk.Event) -> str:
            if self._focused_box_widget is txt and has_v and getattr(event, "delta", 0):
                try:
                    txt.yview_scroll(int(-1 * (event.delta / 120)), "units")
                except Exception:
                    pass
                return "break"
            return self._on_outer_mousewheel(event)

        def _on_shift_wheel(event: tk.Event) -> str:
            if self._focused_box_widget is txt and has_h and getattr(event, "delta", 0):
                try:
                    txt.xview_scroll(int(-1 * (event.delta / 120)), "units")
                except Exception:
                    pass
                return "break"
            return self._on_outer_mousewheel(event)

        txt.bind("<ButtonPress-1>", _on_press)
        txt.bind("<B1-Motion>", _on_drag)
        txt.bind("<FocusOut>", _on_focus_out)
        txt.bind("<MouseWheel>", _on_wheel)
        txt.bind("<Shift-MouseWheel>", _on_shift_wheel)

    def _step_candidate(self, row_idx: int, delta: int) -> None:
        if not (0 <= row_idx < len(self._rows)):
            return
        row = self._rows[row_idx]
        cands = row["candidates"]
        if len(cands) <= 1:
            return
        new_ci = (row["cand_idx"] + delta) % len(cands)
        self._select_candidate(row_idx, new_ci)
        self._apply_conflict_scope(row_idx)

    def _select_candidate(self, row_idx: int, cand_idx: int) -> None:
        row = self._rows[row_idx]
        cands = row["candidates"]
        if not (0 <= cand_idx < len(cands)):
            return
        row["cand_idx"] = cand_idx
        chosen = cands[cand_idx]
        txt_r = row["txt_right"]
        if txt_r.winfo_exists():
            txt_r.config(state="normal")
            txt_r.delete("1.0", tk.END)
            txt_r.insert("1.0", chosen.value)
            txt_r.config(state="disabled")
        rm = self.app._measure_dialogue_metrics(chosen.value)
        ov_badge = ("▼" if rm["has_line_overflow"] else "") + ("▶" if rm["has_width_overflow"] else "")
        row["lbl_right_overflow"].config(text=ov_badge)
        row["lbl_provenance"].config(text=chosen.provenance)
        row["lbl_dup_counter"].config(text=f"{cand_idx + 1}/{len(cands)}")

    def _apply_conflict_scope(self, row_idx: int) -> None:
        """Apply 3-tier duplicate conflict scope (This Box / This Story / Global in-memory opt-in)."""
        row = self._rows[row_idx]
        cands = row["candidates"]
        if not cands:
            return
        chosen = cands[row["cand_idx"]]
        scope = row["var_scope"].get()
        norm_k = row["norm_key"]
        if scope in ("This Story", "Global"):
            for other_idx, other in enumerate(self._rows):
                if other_idx == row_idx or other["norm_key"] != norm_k:
                    continue
                for ci, c in enumerate(other["candidates"]):
                    if c.value == chosen.value:
                        self._select_candidate(other_idx, ci)
                        break

