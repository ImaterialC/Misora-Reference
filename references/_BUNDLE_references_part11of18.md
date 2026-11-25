# BUNDLE references (11/18) | Files: references/misora_parts/misora_part08_L10143-L11633.py

--- FILE: references/misora_parts/misora_part08_L10143-L11633.py [PART 1 | L1-1330/1494 | SHA:e73a5cd43d91] ---
# misora.py PART 08/12 | ORIG L10143-L11633/17315 | SHA:ec4d9bfc8ec6
# SYMS: L10143:MisoraApp.on_toggle_lock_current_box, L10179:MisoraApp._resync_box_indices_from_uids, L10193:MisoraApp._get_dialogue_measure_font, L10210:MisoraApp._measure_dialogue_metrics, L10275:MisoraApp._apply_overflow_highlights, L10291:MisoraApp._apply_gutter_overflow_tag, L10306:MisoraApp._draw_single_pixel_ruler, L10349:MisoraApp._redraw_pixel_rulers, L10371:MisoraApp.on_revert_box, L10375:MisoraApp.on_insert_playername, L10378:MisoraApp._sync_modified_boxes_to_xuat, L10452:MisoraApp.on_save, L10600:MisoraApp._save_active_document_state, L10636:MisoraApp._find_open_doc_key, L10653:MisoraApp._save_document_entry, L10735:MisoraApp.on_reload, L10742:MisoraApp.on_start_search, L10876:MisoraApp._reset_search_results_state, L10888:MisoraApp.on_cancel_search, L10895:MisoraApp._run_background_search, L10946:MisoraApp._process_search_queue, L11043:MisoraApp._render_search_results, L11106:MisoraApp._on_results_click, L11125:MisoraApp._on_results_step, L11138:MisoraApp._select_result_index, L11225:MisoraApp.on_clear_search, L11236:MisoraApp._sync_recent_files_menu, L11257:MisoraApp._clear_recent_files, L11262:MisoraApp.on_open_file, L11300:MisoraApp.on_open_folder, L11309:MisoraApp._get_project_display_path, L11325:MisoraApp._on_folder_path_var_trace, L11342:MisoraApp._sync_scope_widgets, L11376:MisoraApp.on_browse_scope_path, L11384:MisoraApp.on_browse_project_folder, L11399:MisoraApp.on_show_find, L11410:MisoraApp.on_show_find_in_files, L11414:MisoraApp.on_show_replace, L11424:MisoraApp._hide_search_bar, L11431:MisoraApp._apply_compiled_replacement, L11478:MisoraApp._confirm_closed_files_for_op, L11518:MisoraApp.on_replace_next

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
                self._original_box_texts = {i: self._original_jp_by_uid.get(_get_box_uid(b), "") for i, b in enumerate(self.current_doc.boxes)}
        else:
            self._locked_boxes = set()
            self._modified_boxes = set()
            self._original_box_texts = {}

    def _get_dialogue_measure_font(self) -> tkfont.Font:
        """Return a cached tkfont.Font matching the active dialogue editor font."""
        d_fam = getattr(self, "dialogue_font_family", "Consolas")
        d_sz = int(getattr(self, "dialogue_font_size", 11))
        cached = getattr(self, "_dialogue_measure_font", None)
        if cached is None:
            cached = tkfont.Font(root=self, family=d_fam, size=d_sz)
            self._dialogue_measure_font = cached
        else:
            try:
                if cached.cget("family") != d_fam or int(cached.cget("size")) != d_sz:
                    cached.configure(family=d_fam, size=d_sz)
            except Exception:
                cached = tkfont.Font(root=self, family=d_fam, size=d_sz)
                self._dialogue_measure_font = cached
        return cached

    def _measure_dialogue_metrics(self, text: str) -> Dict[str, Any]:
        """Shared pixel-calibrated dialogue measurement helper (S17 / BUG-40, FEAT-09).

        Uses active editor font to compute `safe_w = font.measure('1234567890' * 5)`
        (50 digit-widths, an estimate of the in-game font). Strips NGUI tags to 0px,
        preserves ruby base text, and gives `{playername}`/`{N}` placeholders a realistic
        non-zero width. Measures rendered prefixes with `font.measure(prefix)` for
        kerning-accurate width and exact raw-index overflow mapping.
        """
        f = self._get_dialogue_measure_font()
        safe_w = max(1, int(f.measure("1234567890" * 5)))
        digit_w = safe_w / 50.0
        placeholder_sample = "PlayerName"

        raw_lines = text.split("\n") if text else [""]
        line_metrics: List[Dict[str, Any]] = []

        for line_no, raw_line in enumerate(raw_lines, start=1):
            units: List[Tuple[int, str]] = []
            pos = 0
            for m in NGUI_TOKEN_RE.finditer(raw_line):
                if m.start() > pos:
                    for j in range(pos, m.start()):
                        units.append((j, raw_line[j]))
                tok = m.group(0)
                ruby_m = RUBY_RE.fullmatch(tok)
                if ruby_m:
                    base_start = m.start(3)
                    base_end = m.end(3)
                    if base_start >= 0 and base_end >= base_start:
                        for j in range(base_start, base_end):
                            units.append((j, raw_line[j]))
                elif PLACEHOLDER_RE.fullmatch(tok):
                    units.append((m.start(), placeholder_sample))
                pos = m.end()
            if pos < len(raw_line):
                for j in range(pos, len(raw_line)):
                    units.append((j, raw_line[j]))

            rendered_parts: List[str] = []
            overflow_raw_start: Optional[int] = None
            pixel_width = 0
            for raw_idx, piece in units:
                rendered_parts.append(piece)
                pixel_width = int(f.measure("".join(rendered_parts)))
                if overflow_raw_start is None and pixel_width > safe_w:
                    overflow_raw_start = raw_idx

            line_metrics.append({
                "line_no": line_no,
                "pixel_width": pixel_width,
                "overflow_raw_start": overflow_raw_start,
                "raw_len": len(raw_line),
            })

        line_count = len(raw_lines)
        return {
            "safe_w": safe_w,
            "digit_w": digit_w,
            "line_count": line_count,
            "has_line_overflow": line_count >= 4,
            "has_width_overflow": any(l["overflow_raw_start"] is not None for l in line_metrics),
            "lines": line_metrics,
        }

    def _apply_overflow_highlights(self, widget: Optional[tk.Text]) -> None:
        """Apply inline pixel-calibrated horizontal overflow highlights on a Text widget."""
        if not widget or not widget.winfo_exists():
            return
        try:
            widget.tag_remove("line_overflow", "1.0", tk.END)
            text = widget.get("1.0", "end-1c")
            metrics = self._measure_dialogue_metrics(text)
            for info in metrics["lines"]:
                ov_start = info["overflow_raw_start"]
                if ov_start is not None:
                    ln = info["line_no"]
                    widget.tag_add("line_overflow", f"{ln}.{ov_start}", f"{ln}.end")
        except Exception:
            pass

    def _apply_gutter_overflow_tag(self, gutter_widget: Optional[tk.Text]) -> None:
        """Color vertical line-number gutter red from line 4+ (3 or more linebreaks)."""
        if not gutter_widget or not gutter_widget.winfo_exists():
            return
        try:
            ov_fg = "#ff5c7c" if not self._is_light_theme() else "#c9184a"
            d_sz = int(getattr(self, "dialogue_font_size", 11))
            gutter_widget.tag_configure("gutter_overflow", foreground=ov_fg, font=("Consolas", max(8, d_sz - 1), "bold"))
            gutter_widget.tag_remove("gutter_overflow", "1.0", tk.END)
            total_lines = int(gutter_widget.index("end-1c").split(".")[0])
            if total_lines >= 4:
                gutter_widget.tag_add("gutter_overflow", "4.0", tk.END)
        except Exception:
            pass

    def _draw_single_pixel_ruler(self, canvas: tk.Canvas, x0: int) -> None:
        """Render tick marks and 50 digit-width (est.) overflow zone on a Canvas ruler."""
        if not canvas or not canvas.winfo_exists():
            return
        t = self.theme
        light = self._is_light_theme()
        gutter_bg = "#e8e8e8" if light else "#2d2d30"
        gutter_fg = "#707070" if light else "#858585"
        red_zone_bg = "#ffd6dc" if light else "#4a1c24"
        red_fg = "#c9184a" if light else "#ff5c7c"
        marker_fg = t["misora_pink"]

        canvas.configure(bg=gutter_bg)
        canvas.delete("all")

        metrics = self._measure_dialogue_metrics("")
        safe_w = metrics["safe_w"]
        digit_w = metrics["digit_w"]
        ch = max(20, int(canvas.winfo_height() or 20))
        cw = max(int(canvas.winfo_width() or 0), int(x0 + safe_w + 180))

        # Red overflow zone past 50 digit-widths
        ov_x = x0 + safe_w
        canvas.create_rectangle(ov_x, 0, cw, ch, fill=red_zone_bg, outline="")
        canvas.create_line(x0, ch - 1, cw, ch - 1, fill=gutter_fg)

        col = 0
        while True:
            tx = x0 + int(round(col * digit_w))
            if tx > cw - 8:
                break
            is_major = (col % 10 == 0)
            tick_h = 8 if is_major else 4
            tick_col = red_fg if col > 50 else (marker_fg if col == 50 else gutter_fg)
            canvas.create_line(tx, ch - tick_h - 1, tx, ch - 1, fill=tick_col, width=2 if col == 50 else 1)
            if is_major:
                lbl = "50d" if col == 50 else str(col)
                canvas.create_text(tx + 2, 2, text=lbl, anchor="nw", fill=tick_col, font=("Segoe UI", 7, "bold" if col == 50 else "normal"))
            col += 5

        canvas.create_line(ov_x, 0, ov_x, ch, fill=marker_fg, width=2)
        canvas.create_text(ov_x + 4, 2, text="est. >50d", anchor="nw", fill=red_fg, font=("Segoe UI", 7, "bold"))

    def _redraw_pixel_rulers(self) -> None:
        """Redraw both Clean and All Script Canvas rulers aligned to editor text origins."""
        if hasattr(self, "ruler_clean") and self.ruler_clean.winfo_exists():
            x0_clean = (self.gutter_clean.winfo_reqwidth() + 2 if getattr(self, "show_line_numbers", True) and hasattr(self, "gutter_clean") else 0) + 11
            try:
                if self.txt_dialogue.winfo_ismapped() and self.ruler_clean.winfo_ismapped():
                    x0_clean = (self.txt_dialogue.winfo_rootx() - self.ruler_clean.winfo_rootx()) + int(self.txt_dialogue.cget("bd") or 1) + int(self.txt_dialogue.cget("padx") or 10)
            except Exception:
                pass
            self._draw_single_pixel_ruler(self.ruler_clean, max(0, x0_clean))

        if hasattr(self, "ruler_cont") and self.ruler_cont.winfo_exists():
            x0_cont = (24 if getattr(self, "show_line_numbers", True) else 0) + 17
            try:
                cards = getattr(self, "_card_widgets", {})
                first_txt = next((c.get("txt") for c in cards.values() if c.get("txt") and c["txt"].winfo_ismapped()), None)
                if first_txt is not None and self.ruler_cont.winfo_ismapped():
                    x0_cont = (first_txt.winfo_rootx() - self.ruler_cont.winfo_rootx()) + int(first_txt.cget("bd") or 1) + int(first_txt.cget("padx") or 8)
            except Exception:
                pass
            self._draw_single_pixel_ruler(self.ruler_cont, max(0, x0_cont))

    def on_revert_box(self) -> None:
        if self.current_file_path:
            self.open_file(self.current_file_path, reload_from_disk=True)

    def on_insert_playername(self) -> None:
        self.apply_ngui_wrapper("{playername}", "")

    def _sync_modified_boxes_to_xuat(
        self,
        doc: Any,
        boxes_or_indices: Iterable[Any],
        orig_jp_map: Dict[int, str],
        backup_dir: Optional[Path] = None,
    ) -> Set[str]:
        """
        Synchronize modified boxes to XUAT dictionaries with immutable b_uid JP key resolution
        and conflict preview gate (BUG-25 / DEP-7).
        Returns set of synced file names.
        """
        if not self.var_sync_xuat.get() or not self.xuat_search_roots or not doc or not getattr(doc, "boxes", None):
            return set()

        synced_files: Set[str] = set()
        for item in boxes_or_indices:
            if isinstance(item, int):
                if not (0 <= item < len(doc.boxes)):
                    continue
                box_obj = doc.boxes[item]
                b_idx = item
            else:
                box_obj = item
                b_idx = getattr(box_obj, "index", -1)

            b_uid = _get_box_uid(box_obj)
            orig_key = ""
            if b_uid is not None:
                # Prefer document's orig_jp_map before global sync_manager cache
                orig_key = orig_jp_map.get(b_uid, "") or self.sync_manager.get_jp_key(b_uid, "")
                if not orig_key:
                    # Newly inserted or untracked box with b_uid: skip XUAT sync, NO positional fallback!
                    continue
            else:
                # b_uid is None: only then fall back to positional lookup
                if hasattr(self, "_original_box_texts") and 0 <= b_idx < len(doc.boxes):
                    orig_key = self._original_box_texts.get(b_idx, "")
                if not orig_key:
                    continue

            # Preview matches and gate with conflict confirmation
            previews = self.sync_manager.preview_matches(
                japanese_key=orig_key,
                search_roots=self.xuat_search_roots,
            )
            has_conflict = any(p.is_conflict for p in previews)
            if has_conflict:
                conflict_files = ", ".join(sorted({p.file_path.name for p in previews if p.is_conflict}))
                prompt_msg = (
                    f"Conflicting translations found in XUAT dictionaries for:\n"
                    f"'{orig_key}'\n\n"
                    f"Conflicting file(s): {conflict_files}\n\n"
                    f"Do you want to overwrite all occurrences with:\n"
                    f"'{box_obj.clean_text}'?"
                )
                if not messagebox.askyesno("XUAT Translation Conflict", prompt_msg):
                    continue

            matches = self.sync_manager.find_and_update(
                japanese_key=orig_key,
                new_english_text=box_obj.clean_text,
                search_roots=self.xuat_search_roots,
                backup=True,
                backup_dir=backup_dir,
            )
            for m in matches:
                synced_files.add(m.file_path.name)

        return synced_files

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
                    bak_path = make_collision_resistant_backup_path(self.current_file_path, backup_dir, tag="bak")
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
                if self.current_file_path.is_file() and backup_dir:
                    bak_path = make_collision_resistant_backup_path(self.current_file_path, backup_dir, tag="bak")
                    shutil.copy2(self.current_file_path, bak_path)
                written_size = save_bundle_story(
                    self.current_unity_env,
                    self.current_text_obj,
                    self.current_doc,
                    self.current_file_path,
                    backup_dir=None
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
                    bak_path = make_collision_resistant_backup_path(self.current_file_path, backup_dir, tag="bak")
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
                    if self.current_doc and getattr(self.current_doc, "boxes", None) and not getattr(self, "_original_jp_by_uid", None):
                        self._original_jp_by_uid = {
                            _get_box_uid(b): b.clean_text for b in self.current_doc.boxes if _get_box_uid(b) is not None
                        }
                        for b_uid, jp in self._original_jp_by_uid.items():
                            self.sync_manager.register_jp_key(b_uid, jp)

                    boxes_to_sync = sorted(self._modified_boxes) if self._modified_boxes else [self.current_box_idx]
                    synced_files = self._sync_modified_boxes_to_xuat(
                        doc=self.current_doc,
                        boxes_or_indices=boxes_to_sync,
                        orig_jp_map=getattr(self, "_original_jp_by_uid", {}),
                        backup_dir=backup_dir,
                    )
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

    def _find_open_doc_key(self, path: Union[str, Path]) -> Optional[Path]:
        """Find matching canonical Path key in open_documents normalized for Windows path casing (BUG-24)."""
        if not path or not hasattr(self, "open_documents") or not self.open_documents:
            return None
        try:
            target_norm = os.path.normcase(str(Path(path).resolve()))
        except Exception:
            target_norm = os.path.normcase(str(path))
        for k in self.open_documents.keys():
            try:
                k_norm = os.path.normcase(str(Path(k).resolve()))
            except Exception:
                k_norm = os.path.normcase(str(k))
            if k_norm == target_norm:
                return k if isinstance(k, Path) else Path(k)
        return None

    def _save_document_entry(self, path: Union[str, Path]) -> bool:
        """Save an open document entry to disk without switching active UI context (S06 / BUG-12)."""
        cur_p = Path(path).resolve()
        if cur_p == (Path(self.current_file_path).resolve() if self.current_file_path else None):
            return self.on_save()

        matched_k = self._find_open_doc_key(cur_p)
        if matched_k is None or matched_k not in self.open_documents:
            self.logger.warning("File I/O", f"Cannot save non-open document: {cur_p}")
            return False

        entry = self.open_documents[matched_k]
        backup_dir = self._get_backup_dir()
        modified_uids = set(entry.get("modified_box_uids", set()))

        try:
            if entry.get("is_bundle", False):
                env = entry.get("env")
                obj = entry.get("obj")
                doc = entry.get("doc")
                if not doc:
                    return False
                if cur_p.is_file() and backup_dir:
                    bak_path = make_collision_resistant_backup_path(cur_p, backup_dir, tag="bak")
                    shutil.copy2(cur_p, bak_path)
                written_size = save_bundle_story(
                    env, obj, doc, cur_p, backup_dir=None
                )
                entry["dirty"] = False
                entry["modified_box_uids"] = set()
                self._record_saved_checkpoint(cur_p, doc, "")
                self.undo_journal.mark_saved(str(cur_p))
                self.logger.info("File I/O", f"Saved inactive bundle '{cur_p}' ({written_size} bytes)")
            elif entry.get("doc") is not None:
                doc = entry.get("doc")
                if cur_p.is_file() and backup_dir:
                    bak_path = make_collision_resistant_backup_path(cur_p, backup_dir, tag="bak")
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
                    bak_path = make_collision_resistant_backup_path(cur_p, backup_dir, tag="bak")
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
                    boxes_to_sync = [b for b in doc.boxes if _get_box_uid(b) in modified_uids]
                    self._sync_modified_boxes_to_xuat(
                        doc=doc,
                        boxes_or_indices=boxes_to_sync,
                        orig_jp_map=orig_by_uid,
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

    def _render_search_results(self) -> None:
        """Render grouped search hits with WCAG contrast-safe inline keyword highlighting."""
        y_frac = self.txt_results.yview()[0]
        self._result_line_map.clear()
        self._result_idx_to_line.clear()

        self.txt_results.config(state="normal")
        self.txt_results.delete("1.0", tk.END)

        line_no = 1
        for grp in self.search_file_groups:
            fp: Path = grp["path"]
            indices: List[int] = grp["indices"]
            collapsed: bool = grp["collapsed"]
            arrow = "▶" if collapsed else "▼"
            count_word = "match" if len(indices) == 1 else "matches"
            header_text = f"{arrow} {fp.name} ({len(indices)} {count_word})\n"

            self.txt_results.insert(f"{line_no}.0", header_text, ("file_header",))
            self._result_line_map[line_no] = ("header", grp["key"])
            line_no += 1

            if collapsed:
                continue

            for res_idx in indices:
                r = self.active_search_results[res_idx]
                box_str = f"[Box #{r.box_index + 1}]" if r.box_index is not None else f"[Line {r.line_number}]"
                prefix_indent = "  "
                speaker_prefix = f" {r.speaker}: " if r.speaker else " "
                snippet = r.match_snippet

                row_tags = ("selected_row",) if res_idx == self._selected_result_idx else ()

                self.txt_results.insert(f"{line_no}.0", prefix_indent, row_tags)
                self.txt_results.insert(f"{line_no}.end", box_str, ("box_badge",) + row_tags)
                if r.speaker:
                    self.txt_results.insert(f"{line_no}.end", speaker_prefix, ("speaker_tag",) + row_tags)
                else:
                    self.txt_results.insert(f"{line_no}.end", speaker_prefix, row_tags)

                snip_col_start = len(prefix_indent) + len(box_str) + len(speaker_prefix)
                self.txt_results.insert(f"{line_no}.end", snippet + "\n", row_tags)

                if r.match_in_speaker and r.speaker:
                    sp_offset = len(prefix_indent) + len(box_str) + 1
                    hs = sp_offset + max(0, r.snippet_start)
                    he = sp_offset + max(r.snippet_start, r.snippet_end)
                    if he > hs:
                        self.txt_results.tag_add("match_hl", f"{line_no}.{hs}", f"{line_no}.{he}")
                else:
                    hs = snip_col_start + max(0, r.snippet_start)
                    he = snip_col_start + max(r.snippet_start, r.snippet_end)
                    if he > hs:
                        self.txt_results.tag_add("match_hl", f"{line_no}.{hs}", f"{line_no}.{he}")

                self._result_line_map[line_no] = ("item", res_idx)
                self._result_idx_to_line[res_idx] = line_no
                line_no += 1

        self.txt_results.config(state="disabled")
        self.txt_results.yview_moveto(y_frac)

    def _on_results_click(self, event: tk.Event) -> str:
        """Handle clicking a file header (collapse/expand) or a match row (jump & highlight)."""
        self.txt_results.focus_set()
        idx_str = self.txt_results.index(f"@{event.x},{event.y}")
        line_no = int(idx_str.split(".")[0])
        entry = self._result_line_map.get(line_no)
        if not entry:
            return "break"

        kind, payload = entry
        if kind == "header":
            grp = self._file_group_lookup.get(payload)
            if grp is not None:
                grp["collapsed"] = not grp["collapsed"]
                self._render_search_results()
        elif kind == "item":
            self._select_result_index(int(payload), jump=True)
        return "break"

    def _on_results_step(self, delta: int) -> str:
        """Navigate up/down through visible search hits using keyboard arrow keys."""
        if not self.active_search_results:
            return "break"

        if self._selected_result_idx is None:
            next_idx = 0
        else:
            next_idx = max(0, min(len(self.active_search_results) - 1, self._selected_result_idx + delta))

        self._select_result_index(next_idx, jump=True)
        return "break"

    def _select_result_index(self, idx: int, jump: bool = True) -> None:
        """Highlight selected search row and jump to the matching file/box."""
        if not (0 <= idx < len(self.active_search_results)):
            return

        self._selected_result_idx = idx
        res = self.active_search_results[idx]

        grp = self._file_group_lookup.get(str(res.file_path))
        if grp and grp["collapsed"]:
            grp["collapsed"] = False
            self._render_search_results()
        else:
            self.txt_results.config(state="normal")
            self.txt_results.tag_remove("selected_row", "1.0", tk.END)
            target_line = self._result_idx_to_line.get(idx)
            if target_line is not None:
                self.txt_results.tag_add("selected_row", f"{target_line}.0", f"{target_line}.end")
                self.txt_results.see(f"{target_line}.0")
            self.txt_results.config(state="disabled")

        if not jump:
            return

        if self.var_preview_compiled.get():
            self.var_preview_compiled.set(False)

        if not self.current_file_path or self.current_file_path != res.file_path:
            self.open_file(res.file_path)

        if (res.box_index == -1 or res.line_number == 0) and self.current_doc and self.current_doc.has_metadata():
            self.is_box0_active = True
            if self.var_continuous_view.get():
                self._update_views()
                self._focus_continuous_box(-1, move_cursor=True, char_offset=res.start_pos)
            else:
                self._update_views()
                if "Title" in res.speaker:
                    self.entry_box0_title.focus_set()
                    self.entry_box0_title.selection_range(res.start_pos, res.end_pos)
                elif "Subtitle" in res.speaker:
                    self.entry_box0_subtitle.focus_set()
                    self.entry_box0_subtitle.selection_range(res.start_pos, res.end_pos)
                else:
                    self.txt_box0_summary.focus_set()
                    self.txt_box0_summary.tag_remove("search_hit", "1.0", tk.END)
                    self.txt_box0_summary.tag_add(
                        "search_hit",
                        f"1.0 + {res.start_pos}c",
                        f"1.0 + {res.end_pos}c"
                    )
            return

        self.is_box0_active = False
        if res.box_index is not None and self.current_doc:
            self.current_box_idx = res.box_index
            if self.var_continuous_view.get():
                self._update_views()
                if res.match_in_speaker:
                    self._focus_continuous_box(res.box_index, move_cursor=True)
                    self.entry_speaker.focus_set()
                    self.entry_speaker.selection_range(res.start_pos, res.end_pos)
                else:
                    self._focus_continuous_box(
                        res.box_index,
                        move_cursor=True,
                        char_offset=res.start_pos,
                        explicit_span=(res.start_pos, res.end_pos),
                    )
            else:
                self._update_views()
                if res.match_in_speaker:
                    self.entry_speaker.focus_set()
                    self.entry_speaker.selection_range(res.start_pos, res.end_pos)
                else:
                    self._highlight_dialogue_matches((res.start_pos, res.end_pos))
                    self.txt_dialogue.focus_set()
        elif not self.current_doc and res.line_number > 0:
            self._update_views()
            target_widget = self.txt_continuous if self.var_continuous_view.get() else self.txt_dialogue
            target_widget.tag_remove("search_hit", "1.0", tk.END)
            s_idx = f"{res.line_number}.{res.start_pos}"
            e_idx = f"{res.line_number}.{res.end_pos}"
            target_widget.tag_add("search_hit", s_idx, e_idx)
            target_widget.see(s_idx)
            target_widget.focus_set()

    def on_clear_search(self) -> None:
        self._is_searching = False
        self.active_search_options = None
        self._reset_search_results_state()
        self.txt_dialogue.tag_remove("search_hit", "1.0", tk.END)
        self.txt_continuous.tag_remove("search_hit", "1.0", tk.END)
        self.lbl_results_title.config(text="Search Results (0 matches)")

    # -------------------------------------------------------------------------
    # Dialogs & Helpers
    # -------------------------------------------------------------------------
    def _sync_recent_files_menu(self) -> None:
        """Dynamically populate Recent Files submenu."""
        if not hasattr(self, "recent_menu"):
            return
        self.recent_menu.delete(0, tk.END)
        recents = getattr(self, "recent_files", [])
        valid_recents = [p for p in recents if isinstance(p, Path) and p.exists()]
        if not valid_recents:
            self.recent_menu.add_command(label="(No recent files)", state="disabled")
            return
        for fp in valid_recents[:12]:
            self.recent_menu.add_command(
                label=f"{fp.name}  ({fp.parent})",
                command=lambda p=fp: self.open_file(p),
            )
        self.recent_menu.add_separator()
        self.recent_menu.add_command(
            label="Clear Recent Files",
            command=self._clear_recent_files,
        )

    def _clear_recent_files(self) -> None:
        self.recent_files = []
        self._save_user_prefs(silent=True)
        self.show_toast("Cleared recent files history")

    def on_open_file(self) -> None:
        init_dir = str(self.last_opened_dir) if getattr(self, "last_opened_dir", None) and self.last_opened_dir.exists() else None
        raw_files = filedialog.askopenfilenames(
            initialdir=init_dir,
            title="Open Story Asset or Script",
            filetypes=[
                ("Priconne Assets & Scripts", "*.unity3d;*.asset;*.txt;*.json"),
                ("Unity3D Bundles", "*.unity3d;*.asset"),
                ("Text Scripts", "*.txt;*.json"),
                ("All Files", "*.*")
            ]
        )
        if not raw_files:
            return
        if isinstance(raw_files, str):
            files = [raw_files] if raw_files else []
        else:
            files = [f for f in raw_files if f]
        if not files:
            return

        opened_any = False
        last_success: Optional[Path] = None
        for f in files:
            try:
                p = Path(f).resolve()
                self.open_file(p, refresh_ui=False)
                if p in self.open_documents:
                    opened_any = True
                    last_success = p
            except Exception as e:
                self.logger.exception(f"Failed to open '{f}':", e)

        if opened_any and last_success is not None:
            self.last_opened_dir = last_success.parent
            self.open_file(last_success, refresh_ui=True)
            self._save_user_prefs(silent=True)

    def on_open_folder(self) -> None:
        """Open a folder from menu; prompts user to open all files or set search scope."""
        init_dir = str(self.selected_search_folder) if getattr(self, "selected_search_folder", None) and self.selected_search_folder.exists() else (
            str(self.last_opened_dir) if getattr(self, "last_opened_dir", None) and self.last_opened_dir.exists() else None
        )
        f = filedialog.askdirectory(initialdir=init_dir, title="Open Folder (Story Files or Search Scope)")
        if f:
            self._process_opened_folder(Path(f), source_label="Open Folder")

    def _get_project_display_path(self) -> str:
        """Return the effective project directory path (BepInEx, MelonLoader, XUAT, etc.)."""
        p = getattr(self, "project_folder", None) or getattr(self, "bepinex_project_folder", None)
        if p and Path(p).exists():
            return str(p)
        if getattr(self, "xuat_search_roots", None) and self.xuat_search_roots:
            first_root = self.xuat_search_roots[0]
            if first_root.exists():
                self.project_folder = first_root
                self.bepinex_project_folder = first_root
                return str(first_root)
        parent_dir = SCRIPT_DIR.parent
        self.project_folder = parent_dir
        self.bepinex_project_folder = parent_dir
        return str(parent_dir)

    def _on_folder_path_var_trace(self) -> None:
        """Synchronize project_folder or selected_search_folder when user edits folder_path_var."""
        if getattr(self, "_syncing_folder_path_var", False):
            return
        scope_v = getattr(self, "scope_var", None)
        if not scope_v:
            return
        s = scope_v.get()
        val = self.folder_path_var.get().strip()
        if s == "project":
            if val:
                p = Path(val)
                self._set_project_folder(p)
        elif s == "folder":
            if val:
                self.selected_search_folder = Path(val)

    def _sync_scope_widgets(self) -> None:
        """Update folder/project path entry and browse button based on scope selection."""
        if not (hasattr(self, "folder_path_entry") and hasattr(self, "btn_browse_search_folder")):
            return
        scope = self.scope_var.get()
        self._syncing_folder_path_var = True
        try:
            if scope == "folder":
                if not self.btn_browse_search_folder.winfo_manager():
                    self.btn_browse_search_folder.pack(side="left", padx=(0, 2))
                if not self.folder_path_entry.winfo_manager():
                    self.folder_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 2))
                self.folder_path_entry.config(state="normal")
                self.btn_browse_search_folder.config(state="normal")
                if getattr(self, "selected_search_folder", None):
                    self.folder_path_var.set(str(self.selected_search_folder))
                else:
                    self.folder_path_var.set("")
            elif scope == "project":
                if not self.btn_browse_search_folder.winfo_manager():
                    self.btn_browse_search_folder.pack(side="left", padx=(0, 2))
                if not self.folder_path_entry.winfo_manager():
                    self.folder_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 2))
                self.folder_path_entry.config(state="normal")
                self.btn_browse_search_folder.config(state="normal")
                self.folder_path_var.set(self._get_project_display_path())
            else:  # "current"
                self.btn_browse_search_folder.pack_forget()
                self.folder_path_entry.pack_forget()
                self.folder_path_entry.config(state="readonly")
                self.btn_browse_search_folder.config(state="disabled")
        finally:
            self._syncing_folder_path_var = False

    def on_browse_scope_path(self) -> None:
        """Browse button handler for the active search scope ([...] on left of directory entry)."""
        scope = self.scope_var.get()
        if scope == "project":
            self.on_browse_project_folder()
        elif scope == "folder":
            self.on_open_folder()

    def on_browse_project_folder(self) -> None:
        """Browse and configure the Project Root / Mod Translation Folder."""
        init_dir = self._get_project_display_path()
        d = filedialog.askdirectory(initialdir=init_dir, title="Select Project Root / Mod Folder (BepInEx, MelonLoader, etc.)")
        if d:
            p = Path(d)
            self._set_project_folder(p)
            self.folder_path_var.set(str(p))
            self._save_user_prefs(silent=True)
            self.lbl_status.config(text=f"Project folder set to: {p}")
            self.show_toast(f"Project folder set to: {p.name}")

    # -------------------------------------------------------------------------
    # Search & Replace Actions (Find, Replace, Replace All, Multi-File Confirmation)
    # -------------------------------------------------------------------------
    def on_show_find(self) -> None:
        if not getattr(self, "_search_bar_visible", False):
            # search_frame and h_paned are both direct children of self (root)
            self.search_frame.pack(before=self.h_paned, fill="x", padx=8, pady=(6, 4))
            self._search_bar_visible = True
        self._sync_scope_widgets()
        if getattr(self, "_replace_row_visible", False):
            self._hide_replace_row()
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)

    def on_show_find_in_files(self) -> None:
        self.scope_var.set("project")
        self.on_show_find()

    def on_show_replace(self) -> None:
        if not getattr(self, "_search_bar_visible", False):
            self.search_frame.pack(before=self.h_paned, fill="x", padx=8, pady=(6, 4))
            self._search_bar_visible = True
        self._sync_scope_widgets()
        if not getattr(self, "_replace_row_visible", False):
            self._show_replace_row()
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)

    def _hide_search_bar(self) -> None:
        if hasattr(self, "search_frame"):
            self.search_frame.pack_forget()
            self._search_bar_visible = False
            target = self.txt_continuous if self.var_continuous_view.get() else self.txt_dialogue
            target.focus_set()

    def _apply_compiled_replacement(
        self,
        text: str,
        matcher: Callable[[str], List[Any]],
        replacement: str,
        is_regex: bool = False,
        ignore_ws: bool = False,
        count: int = 0,
        regex_pattern: Optional[re.Pattern] = None,
    ) -> Tuple[str, int]:
        """Apply replacement across text honoring Match Case, Regex, and Ignore Whitespace (BUG-24 / QW-R06).

        Replaces non-overlapping spans returned by matcher in reverse order to preserve indexing.
        When is_regex is True, supports group backreferences via regex substitution.
        Returns (new_text, occurrences_replaced).
        """
        if not text:
            return text, 0

        if is_regex:
            rx = regex_pattern
            if rx is None:
                if hasattr(matcher, "__closure__") and matcher.__closure__:
                    for cell in matcher.__closure__:
                        if isinstance(cell.cell_contents, re.Pattern):
                            rx = cell.cell_contents
                            break
            if rx is None:
                q = getattr(self, "search_var", None).get() if getattr(self, "search_var", None) else ""
                flags = 0 if getattr(self, "var_case", None) and self.var_case.get() else re.IGNORECASE
                rx = re.compile(q, flags)
            new_text, num = rx.subn(replacement, text, count=count)
            return new_text, num

        matches = matcher(text)
        if not matches:
            return text, 0

        if count > 0:

