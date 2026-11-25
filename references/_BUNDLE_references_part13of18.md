# BUNDLE references (13/18) | Files: references/misora_parts/misora_part09_L11634-L13097.py

--- FILE: references/misora_parts/misora_part09_L11634-L13097.py [PART 1 | L1-1209/1467 | SHA:16619525af33] ---
# misora.py PART 09/12 | ORIG L11634-L13097/17315 | SHA:ec4d9bfc8ec6
# SYMS: L11634:MisoraApp.on_replace_all, L11984:MisoraApp.on_undo, L12012:MisoraApp.on_redo, L12040:MisoraApp._restore_bundle_atomic, L12071:MisoraApp._apply_delta, L12323:MisoraApp._sync_edit_menu_states, L12341:MisoraApp._switch_dock_tab, L12360:MisoraApp._toggle_dock_collapse, L12408:MisoraApp._refresh_opened_files_list, L12440:MisoraApp._on_opened_files_click, L12457:MisoraApp.close_file, L12518:MisoraApp.close_others, L12526:MisoraApp.close_all_unmodified, L12537:MisoraApp.close_all_files, L12543:MisoraApp._close_all_documents_without_prompt, L12573:MisoraApp.on_save_project, L12588:MisoraApp.save_project, L12637:MisoraApp.on_open_project, L12648:MisoraApp.open_project, L12787:MisoraApp._on_results_right_click, L12805:MisoraApp._on_opened_files_right_click, L12814:MisoraApp._show_file_context_menu, L12854:MisoraApp._open_containing_folder, L12864:MisoraApp._launch_editor_on_file, L12880:MisoraApp._choose_app_and_open, L12886:MisoraApp._copy_to_clipboard, L12891:MisoraApp._sync_external_editor_menu, L12901:MisoraApp.on_set_external_editor, L12912:MisoraApp.on_clear_external_editor, L12920:MisoraApp.on_launch_datamine, L12990:MisoraApp.on_select_datamine_exe, L13006:MisoraApp.on_open_datamine_folder, L13015:MisoraApp.on_open_backups_folder, L13019:MisoraApp.on_open_project_folder, L13032:MisoraApp.on_open_bepinex_folder, L13036:MisoraApp.on_open_program_folder, L13039:MisoraApp.on_open_xuat_text_folder, L13069:MisoraApp.on_open_redirected_resources_folder, L13091:MisoraApp.on_open_selected_search_folder

    def on_replace_all(self) -> None:
        """Replace all occurrences in current file or across project/folder (BUG-24)."""
        find_text = self.search_var.get()
        replace_text = self.replace_var.get()
        if not find_text:
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

        scope = self.scope_var.get()
        if scope == "current":
            if not self.current_file_path:
                messagebox.showinfo("Replace All", "No active file open.")
                return
            if self.current_doc and self.current_doc.boxes:
                count = 0
                skipped_locked = 0
                self.undo_journal.begin_batch(f"Replace All '{find_text}' in {self.current_file_path.name}")
                for idx, box in enumerate(self.current_doc.boxes):
                    matches = matcher(box.clean_text)
                    if matches:
                        if self.is_box_locked(idx):
                            skipped_locked += 1
                            continue
                        old_sp = box.speaker
                        old_tx = box.clean_text
                        new_tx, _ = self._apply_compiled_replacement(
                            box.clean_text, matcher, replace_text, is_regex=use_regex, ignore_ws=ignore_ws, count=0
                        )
                        self.undo_journal.record(
                            BoxEditDelta(
                                box_index=idx,
                                old_speaker=old_sp,
                                new_speaker=old_sp,
                                old_text=old_tx,
                                new_text=new_tx,
                                file_path=str(self.current_file_path),
                                box_uid=box.uid,
                                source="replace",
                            )
                        )
                        self.current_doc.inject_box(idx, None, new_tx)
                        self._modified_boxes.add(idx)
                        count += 1
                self.undo_journal.end_batch()
                if count > 0:
                    self._mark_document_dirty(self.current_file_path)
                    self._dirty_state_changed()
                    self._update_views()
                    msg = f"Replaced in {count} box(es) in {self.current_file_path.name}"
                    if skipped_locked > 0:
                        msg += f" ({skipped_locked} locked boxes preserved)"
                    self.lbl_status.config(text=msg)
                    self.show_toast(f"✓ {msg}")
                    self.logger.info("Search", f"Replaced all '{find_text}' -> '{replace_text}' in {count} boxes of {self.current_file_path.name}")
                elif skipped_locked > 0:
                    self.lbl_status.config(text=f"All matching boxes ({skipped_locked}) are locked.")
                    messagebox.showinfo("Replace All", f"Matches were found in {skipped_locked} box(es), but they are all protected by Translation Lock.")
                else:
                    messagebox.showinfo("Replace All", f"'{find_text}' not found in current file.")
            elif not self.current_doc and self.current_file_path:
                cur_tx = self._plain_text_content
                matches = matcher(cur_tx)
                if matches:
                    occurrences = len(matches)
                    new_tx, _ = self._apply_compiled_replacement(
                        cur_tx, matcher, replace_text, is_regex=use_regex, ignore_ws=ignore_ws, count=0
                    )
                    self.undo_journal.record(
                        PlainTextDelta(
                            file_path=str(self.current_file_path),
                            old_content=cur_tx,
                            new_content=new_tx,
                        ),
                        label=f"Replace All in {self.current_file_path.name}"
                    )
                    self._plain_text_content = new_tx
                    matched_k = self._find_open_doc_key(self.current_file_path)
                    if matched_k and matched_k in self.open_documents:
                        self.open_documents[matched_k]["plain_text"] = new_tx
                    self._mark_document_dirty(self.current_file_path)
                    self._dirty_state_changed()
                    self._update_views()
                    self.lbl_status.config(text=f"Replaced {occurrences} occurrence(s) in {self.current_file_path.name}")
                else:
                    messagebox.showinfo("Replace All", f"'{find_text}' not found in current file.")
        else:
            # Multi-file Replace All
            target_roots: List[Path] = []
            if scope == "folder":
                fp = self.folder_path_var.get().strip() or (str(self.selected_search_folder) if self.selected_search_folder else "")
                if fp and Path(fp).exists():
                    target_roots = [Path(fp)]
                else:
                    messagebox.showerror("Replace All", "Please select a valid folder for Folder scope.")
                    return
            else:
                target_roots = list(self.xuat_search_roots)
                active_proj = getattr(self, "project_folder", None) or getattr(self, "bepinex_project_folder", None)
                if active_proj and active_proj.exists():
                    text_dir = active_proj / "Text"
                    root = text_dir if text_dir.exists() else active_proj
                    if root not in target_roots:
                        target_roots.insert(0, root)

            inc_bdl = bool(getattr(self, "var_inc_bundles", None) and self.var_inc_bundles.get())
            inc_txt = bool(getattr(self, "var_inc_text", None) and self.var_inc_text.get()) if getattr(self, "var_inc_text", None) is not None else True

            seen_paths: Set[Path] = set()
            candidate_files: List[Path] = []
            for root in target_roots:
                root_p = Path(root).resolve()
                if root_p.is_file():
                    if root_p not in seen_paths:
                        seen_paths.add(root_p)
                        candidate_files.append(root_p)
                elif root_p.is_dir():
                    if inc_bdl:
                        for pat in ("*.unity3d", "*.asset"):
                            for f in root_p.rglob(pat):
                                fp = f.resolve()
                                if fp not in seen_paths and fp.is_file():
                                    seen_paths.add(fp)
                                    candidate_files.append(fp)
                    if inc_txt:
                        for f in root_p.rglob("*.txt"):
                            fp = f.resolve()
                            if fp not in seen_paths and fp.is_file():
                                seen_paths.add(fp)
                                candidate_files.append(fp)

            matching_files: Dict[Path, int] = {}
            total_matches = 0

            for cf in candidate_files:
                try:
                    if cf.suffix.lower() in (".unity3d", ".asset"):
                        bundle_env = None
                        try:
                            b_doc, bundle_env, _, _ = load_bundle_story(cf)
                            open_k = self._find_open_doc_key(cf)
                            locked_uids: Set[int] = set()
                            if open_k and open_k in self.open_documents:
                                locked_uids = set(self.open_documents[open_k].get("locked_box_uids", set()))
                            elif open_k == (Path(self.current_file_path).resolve() if self.current_file_path else None):
                                locked_uids = set(getattr(self, "_locked_box_uids", set()))

                            c = 0
                            for box in b_doc.boxes:
                                b_uid = _get_box_uid(box)
                                if b_uid is not None and b_uid in locked_uids:
                                    continue
                                c += len(matcher(box.clean_text))
                            if c > 0:
                                matching_files[cf] = c
                                total_matches += c
                        finally:
                            if bundle_env is not None:
                                dispose_unity_env(bundle_env)
                    else:
                        decoded = read_text_file_strictly(cf)
                        c = len(matcher(decoded.text))
                        if c > 0:
                            matching_files[cf] = c
                            total_matches += c
                except Exception:
                    pass

            if not matching_files:
                messagebox.showinfo("Replace All", f"No matches for '{find_text}' found across {len(candidate_files)} files.")
                return

            # Refuse/prompt before overwriting dirty open documents (BUG-24)
            dirty_open: List[Path] = []
            for fp in matching_files:
                open_k = self._find_open_doc_key(fp)
                if open_k and open_k in self.open_documents:
                    is_active_dirty = (open_k == (Path(self.current_file_path).resolve() if self.current_file_path else None) and getattr(self, "is_dirty", False))
                    if self.open_documents[open_k].get("dirty", False) or is_active_dirty:
                        dirty_open.append(open_k)

            if dirty_open:
                dirty_list = "\n".join(f"  • {p.name} ({p})" for p in dirty_open)
                ans = messagebox.askyesno(
                    "Unsaved Changes in Open Files",
                    f"The following {len(dirty_open)} open document(s) have unsaved changes that would be overwritten by Replace All:\n\n"
                    f"{dirty_list}\n\n"
                    f"Proceed and overwrite these unsaved changes?",
                    default=messagebox.NO,
                    icon=messagebox.WARNING,
                )
                if not ans:
                    self.lbl_status.config(text="Replace All cancelled: open documents have unsaved changes.")
                    return

            confirm_msg = (
                f"Replace All across multiple files:\n\n"
                f"Search query: '{find_text}'\n"
                f"Replacement:  '{replace_text}'\n\n"
                f"Found ~{total_matches} match(es) across {len(matching_files)} file(s).\n\n"
                f"Proceed with replacement?"
            )
            ans = messagebox.askyesno(
                "Confirm Multi-File Replace All",
                confirm_msg,
                default=messagebox.NO,
                icon=messagebox.WARNING
            )
            if not ans:
                return

            replaced_files_count = 0
            per_file_deltas: List[Any] = []

            for fpath in matching_files:
                try:
                    if fpath.suffix.lower() in (".unity3d", ".asset"):
                        bundle_env = None
                        try:
                            doc, bundle_env, obj, _ = load_bundle_story(fpath)
                            open_k = self._find_open_doc_key(fpath)
                            locked_uids = set()
                            if open_k and open_k in self.open_documents:
                                locked_uids = set(self.open_documents[open_k].get("locked_box_uids", set()))
                            elif open_k == (Path(self.current_file_path).resolve() if self.current_file_path else None):
                                locked_uids = set(getattr(self, "_locked_box_uids", set()))

                            modified = False
                            for idx, box in enumerate(doc.boxes):
                                b_uid = _get_box_uid(box)
                                if b_uid is not None and b_uid in locked_uids:
                                    continue
                                if matcher(box.clean_text):
                                    new_box_tx, _ = self._apply_compiled_replacement(
                                        box.clean_text, matcher, replace_text, is_regex=use_regex, ignore_ws=ignore_ws, count=0
                                    )
                                    doc.inject_box(idx, None, new_box_tx)
                                    modified = True
                            if modified:
                                bak_dir = self._get_backup_dir()
                                orig_bak_path = make_collision_resistant_backup_path(fpath, bak_dir, tag="orig")
                                shutil.copy2(fpath, orig_bak_path)

                                save_bundle_story(bundle_env, obj, doc, fpath, backup_dir=None)

                                mod_bak_path = make_collision_resistant_backup_path(fpath, bak_dir, tag="mod")
                                shutil.copy2(fpath, mod_bak_path)

                                per_file_deltas.append((str(fpath), str(orig_bak_path), str(mod_bak_path), True))
                                replaced_files_count += 1
                        finally:
                            if bundle_env is not None:
                                dispose_unity_env(bundle_env)
                    else:
                        decoded = read_text_file_strictly(fpath)
                        old_txt = decoded.text
                        if matcher(old_txt):
                            new_txt, _ = self._apply_compiled_replacement(
                                old_txt, matcher, replace_text, is_regex=use_regex, ignore_ws=ignore_ws, count=0
                            )
                            bak_dir = self._get_backup_dir()
                            bak_path = make_collision_resistant_backup_path(fpath, bak_dir, tag="bak")
                            shutil.copy2(fpath, bak_path)
                            if decoded.has_bom or (decoded.newline and decoded.newline != "\n"):
                                write_atomic_utf8(
                                    fpath,
                                    new_txt,
                                    encoding=decoded.encoding,
                                    has_bom=decoded.has_bom,
                                    newline=decoded.newline,
                                )
                            else:
                                write_atomic_utf8(fpath, new_txt, encoding=decoded.encoding)
                            per_file_deltas.append((str(fpath), old_txt, new_txt))
                            replaced_files_count += 1
                except Exception as ex:
                    self.logger.error("Search", f"Failed replacing in {fpath}: {ex}")

            # Refresh ALL affected open document caches (including inactive tabs) & do NOT mark disk-saved files dirty
            for item in per_file_deltas:
                fpath_str = item[0]
                fp = Path(fpath_str).resolve()
                open_k = self._find_open_doc_key(fp)
                if open_k and open_k in self.open_documents:
                    entry = self.open_documents[open_k]
                    is_bdl = len(item) >= 4 and bool(item[3])
                    if is_bdl:
                        try:
                            b_doc, b_env, b_obj, _ = load_bundle_story(fp)
                            old_env = entry.get("env")
                            if old_env is not None and old_env is not b_env:
                                dispose_unity_env(old_env)
                            entry["doc"] = b_doc
                            entry["env"] = b_env
                            entry["obj"] = b_obj
                            entry["dirty"] = False
                            self._record_saved_checkpoint(open_k, b_doc)
                            if open_k == (Path(self.current_file_path).resolve() if self.current_file_path else None):
                                self.current_doc = b_doc
                                self.current_unity_env = b_env
                                self.current_text_obj = b_obj
                                self.is_dirty = False
                        except Exception as ex_refresh:
                            self.logger.error("Search", f"Failed refreshing bundle cache for {fp}: {ex_refresh}")
                    else:
                        new_txt = item[2]
                        entry["plain_text"] = new_txt
                        entry["dirty"] = False
                        self._record_saved_checkpoint(open_k, None, plain_text=new_txt)
                        if open_k == (Path(self.current_file_path).resolve() if self.current_file_path else None):
                            self._plain_text_content = new_txt
                            self.is_dirty = False

            if per_file_deltas:
                self.undo_journal.record(
                    BulkFileDelta(
                        description=f"Replace '{find_text}' -> '{replace_text}' in {len(per_file_deltas)} files",
                        per_file=per_file_deltas,
                    )
                )

            active_k = self._find_open_doc_key(self.current_file_path) if self.current_file_path else None
            if active_k and any(Path(it[0]).resolve() == active_k for it in per_file_deltas):
                self._update_views()
                self._dirty_state_changed()

            self.lbl_status.config(text=f"Bulk Replace Complete: Updated {replaced_files_count} file(s).")
            self.logger.info("Search", f"Bulk replaced '{find_text}' -> '{replace_text}' in {replaced_files_count} file(s)")
            messagebox.showinfo("Replace All Complete", f"Successfully replaced '{find_text}' across {replaced_files_count} file(s).")

    # -------------------------------------------------------------------------
    # Undo / Redo Actions (#3A)
    # -------------------------------------------------------------------------
    def on_undo(self) -> None:
        """Undo the most recent operation from MasterUndoJournal (Rule 13, Part B.6)."""
        self._commit_widget_edit()
        cur_fp = str(self.current_file_path) if self.current_file_path else None

        # Inspect next undo op before popping to avoid corrupting undo/redo stack on cancellation (BUG-24)
        with self.undo_journal._lock:
            state = self.undo_journal._get_state(cur_fp)
            next_op = state.undo_stack[-1] if state.undo_stack else None

        if next_op and not self._confirm_closed_files_for_op(next_op, is_undo=True):
            self.lbl_status.config(text="Undo cancelled.")
            return

        op = self.undo_journal.pop_undo(cur_fp)
        if not op:
            self.lbl_status.config(text="Nothing to undo.")
            return
        for delta in reversed(op.deltas):
            self._apply_delta(delta, reverse=True, refresh_ui=False)
        self._update_views()
        self._sync_clean_view_to_current_box()
        self._evaluate_checkpoints_for_op(op)
        self._dirty_state_changed()
        self._sync_edit_menu_states()
        self.lbl_status.config(text=f"Undid: {op.label}")
        self.logger.info("Edit", f"Undid operation: {op.label}")

    def on_redo(self) -> None:
        """Redo the most recent undone operation from MasterUndoJournal (Rule 13, Part B.6)."""
        self._commit_widget_edit()
        cur_fp = str(self.current_file_path) if self.current_file_path else None

        # Inspect next redo op before popping to avoid corrupting undo/redo stack on cancellation (BUG-24)
        with self.undo_journal._lock:
            state = self.undo_journal._get_state(cur_fp)
            next_op = state.redo_stack[-1] if state.redo_stack else None

        if next_op and not self._confirm_closed_files_for_op(next_op, is_undo=False):
            self.lbl_status.config(text="Redo cancelled.")
            return

        op = self.undo_journal.pop_redo(cur_fp)
        if not op:
            self.lbl_status.config(text="Nothing to redo.")
            return
        for delta in op.deltas:
            self._apply_delta(delta, reverse=False, refresh_ui=False)
        self._update_views()
        self._sync_clean_view_to_current_box()
        self._evaluate_checkpoints_for_op(op)
        self._dirty_state_changed()
        self._sync_edit_menu_states()
        self.lbl_status.config(text=f"Redid: {op.label}")
        self.logger.info("Edit", f"Redid operation: {op.label}")

    @staticmethod
    def _restore_bundle_atomic(src_bak_path: Union[str, Path], dst_path: Path) -> None:
        """Atomically restore a binary bundle file from a backup snapshot (S9b)."""
        src_p = Path(src_bak_path)
        if not src_p.is_file():
            raise FileNotFoundError(f"Bundle backup file not found: {src_p}")
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = dst_path.with_name(f"{dst_path.name}.{os.getpid()}_{time.time_ns()}.tmp")
        shutil.copy2(src_p, tmp_path)
        retries = 5
        for attempt in range(retries):
            try:
                os.replace(tmp_path, dst_path)
                break
            except PermissionError:
                if attempt == retries - 1:
                    if tmp_path.exists():
                        try:
                            tmp_path.unlink()
                        except Exception:
                            pass
                    raise
                time.sleep(0.05 * (attempt + 1))
            except Exception:
                if tmp_path.exists():
                    try:
                        tmp_path.unlink()
                    except Exception:
                        pass
                raise

    def _apply_delta(self, delta: Any, reverse: bool = False, refresh_ui: bool = True) -> None:
        """Apply a recorded delta forwards or backwards, preserving cursor position."""
        prev_caret = None
        try:
            target_w = self._get_active_text_widget()
            if target_w and target_w.winfo_exists():
                prev_caret = target_w.index(tk.INSERT)
        except Exception:
            pass

        if isinstance(delta, BoxEditDelta):
            target_sp = delta.old_speaker if reverse else delta.new_speaker
            target_tx = delta.old_text if reverse else delta.new_text
            target_segs = delta.old_seg_texts if reverse else delta.new_seg_texts
            target_file = Path(delta.file_path) if delta.file_path else None
            if target_file and target_file != self.current_file_path:
                self.open_file(target_file)
            if self.current_doc:
                target_idx = delta.box_index
                if delta.box_uid is not None:
                    found_idx = next(
                        (i for i, b in enumerate(self.current_doc.boxes) if b.segs and b.segs[0].record.uid == delta.box_uid),
                        None
                    )
                    if found_idx is not None:
                        target_idx = found_idx
                if 0 <= target_idx < len(self.current_doc.boxes):
                    self.current_doc.inject_box(target_idx, target_sp, target_tx, seg_texts=target_segs)
                    self.current_box_idx = target_idx
                    self._modified_boxes.add(target_idx)
                    self._mark_document_dirty(target_file or self.current_file_path)
                    if refresh_ui:
                        self._update_views()
        elif isinstance(delta, MetadataDelta):
            target_title = delta.old_title if reverse else delta.new_title
            target_sub = delta.old_subtitle if reverse else delta.new_subtitle
            target_summary = delta.old_summary if reverse else delta.new_summary
            target_file = Path(delta.file_path) if delta.file_path else None
            if target_file and target_file != self.current_file_path:
                self.open_file(target_file)
            if self.current_doc:
                self.current_doc.set_metadata(title=target_title, subtitle=target_sub, summary=target_summary)
                self.is_box0_active = True
                self.current_box_idx = 0
                self._mark_document_dirty(target_file or self.current_file_path)
                if refresh_ui:
                    self._update_views()
        elif isinstance(delta, DocumentRecordsDelta):
            target_file = Path(delta.file_path) if delta.file_path else None
            if target_file and target_file != self.current_file_path:
                self.open_file(target_file)
            self._exit_raw_edit_mode(refresh=False)
            if self.current_doc:
                target_recs = delta.old_records if reverse else delta.new_records
                target_removed = delta.old_removed_records if reverse else delta.new_removed_records
                self.current_doc.records = copy.deepcopy(target_recs)
                self.current_doc.removed_records = set(target_removed)
                self.current_doc._rebuild_boxes()

                self._locked_box_uids = set(delta.old_locked_uids if reverse else delta.new_locked_uids)
                self._original_jp_by_uid = dict(delta.old_jp_by_uid if reverse else delta.new_jp_by_uid)
                if hasattr(self, "sync_manager") and self.sync_manager is not None:
                    for b_uid, jp_txt in self._original_jp_by_uid.items():
                        self.sync_manager.register_jp_key(b_uid, jp_txt)
                target_p = target_file or self.current_file_path
                if target_p:
                    cur_p = Path(target_p).resolve()
                    if cur_p in self.open_documents:
                        self.open_documents[cur_p]["locked_box_uids"] = set(self._locked_box_uids)
                        self.open_documents[cur_p]["original_jp_by_uid"] = dict(self._original_jp_by_uid)
                self._resync_box_indices_from_uids()

                target_box_idx = delta.old_box_idx if reverse else delta.new_box_idx
                if self.current_doc.boxes:
                    self.current_box_idx = max(0, min(target_box_idx, len(self.current_doc.boxes) - 1))
                else:
                    self.current_box_idx = 0
                target_is_box0 = delta.old_is_box0 if reverse else delta.new_is_box0
                self.is_box0_active = bool(target_is_box0 and self.current_doc.has_metadata())
                self._mark_document_dirty(target_p)
                if refresh_ui:
                    self._update_views()
        elif isinstance(delta, BoxStructuralDelta):
            target_file = Path(delta.file_path) if delta.file_path else None
            if target_file and target_file != self.current_file_path:
                self.open_file(target_file)
            if self.current_doc:
                is_insert = (delta.op_type == "insert") if not reverse else (delta.op_type != "insert")
                indices = getattr(delta, "indices", None)
                if is_insert:
                    if indices is not None and len(indices) == len(delta.snapshots):
                        for idx, snap in zip(indices, delta.snapshots):
                            self.current_doc.insert_box(idx, snap)
                        self.current_box_idx = indices[0] if indices else delta.box_index
                    else:
                        for offset, snap in enumerate(delta.snapshots):
                            self.current_doc.insert_box(delta.box_index + offset, snap)
                        self.current_box_idx = delta.box_index
                else:
                    if indices is not None:
                        delete_indices = list(indices)
                    else:
                        delete_indices = list(range(delta.box_index, delta.box_index + len(delta.snapshots)))
                    self.current_doc.delete_boxes(delete_indices)
                    target_box = indices[0] if indices else delta.box_index
                    self.current_box_idx = max(0, min(target_box, len(self.current_doc.boxes) - 1))
                self._resync_box_indices_from_uids()
                self._mark_document_dirty(target_file or self.current_file_path)
                if refresh_ui:
                    self._update_views()
                    self._sync_clean_view_to_current_box()
                    self._dirty_state_changed()
        elif isinstance(delta, PlainTextDelta):
            target_tx = delta.old_content if reverse else delta.new_content
            target_file = Path(delta.file_path) if delta.file_path else None
            if target_file and target_file != self.current_file_path:
                self.open_file(target_file)
            self._plain_text_content = target_tx
            target_p = target_file or self.current_file_path
            if target_p:
                p_res = Path(target_p).resolve()
                if p_res in self.open_documents:
                    self.open_documents[p_res]["plain_text"] = target_tx
            self._mark_document_dirty(target_p)
            if refresh_ui:
                self._update_views()
        elif isinstance(delta, BulkFileDelta):
            applied_files: List[Tuple[Path, bool, Any, Optional[str], bool, Optional[str]]] = []
            try:
                for item in delta.per_file:
                    is_bundle = len(item) >= 4 and bool(item[3])
                    fpath_str = item[0]
                    fp = Path(fpath_str).resolve()
                    if is_bundle:
                        orig_bak_str = item[1]
                        mod_bak_str = item[2]
                        src_bak = orig_bak_str if reverse else mod_bak_str
                        prev_bak = mod_bak_str if reverse else orig_bak_str
                        self._restore_bundle_atomic(src_bak, fp)
                        applied_files.append((fp, True, prev_bak, None, False, None))

                        # S9b & S09: Synchronize in-memory cache using canonical keys 'env' and 'obj'
                        open_k = self._find_open_doc_key(fp)
                        if open_k and open_k in self.open_documents:
                            try:
                                b_doc, b_env, b_obj, _ = load_bundle_story(fp)
                                old_env = self.open_documents[open_k].get("env")
                                if old_env is not None and old_env is not b_env:
                                    dispose_unity_env(old_env)
                                self.open_documents[open_k]["doc"] = b_doc
                                self.open_documents[open_k]["env"] = b_env
                                self.open_documents[open_k]["obj"] = b_obj
                                self.open_documents[open_k]["dirty"] = False
                                self._record_saved_checkpoint(open_k, b_doc)
                                if open_k == (Path(self.current_file_path).resolve() if self.current_file_path else None):
                                    self.current_doc = b_doc
                                    self.current_unity_env = b_env
                                    self.current_text_obj = b_obj
                                    self.is_dirty = False
                            except Exception as ex_load:
                                self.logger.error("File I/O", f"Failed reloading bundle cache for {fp}: {ex_load}")
                    else:
                        old_tx = item[1]
                        new_tx = item[2]
                        text_to_set = old_tx if reverse else new_tx
                        prev_text = new_tx if reverse else old_tx
                        open_k = self._find_open_doc_key(fp)
                        doc_entry = self.open_documents.get(open_k, {}) if open_k else {}
                        enc = doc_entry.get("encoding")
                        has_bom = doc_entry.get("has_bom")
                        nl = doc_entry.get("newline")
                        if enc is None and fp.is_file():
                            try:
                                det = read_text_file_strictly(fp)
                                enc = det.encoding
                                has_bom = det.has_bom if has_bom is None else has_bom
                                nl = det.newline if nl is None else nl
                            except Exception:
                                enc = "utf-8"
                        enc = enc or "utf-8"
                        has_bom = bool(has_bom) if has_bom is not None else False
                        if has_bom or (nl and nl != "\n"):
                            write_atomic_utf8(fp, text_to_set, encoding=enc, has_bom=has_bom, newline=nl)
                        else:
                            write_atomic_utf8(fp, text_to_set, encoding=enc)
                        applied_files.append((fp, False, prev_text, enc, has_bom, nl))

                        # S5 & S09: Synchronize in-memory cache and checkpoints if open
                        if open_k and open_k in self.open_documents:
                            self.open_documents[open_k]["plain_text"] = text_to_set
                            self.open_documents[open_k]["dirty"] = False
                            self._record_saved_checkpoint(open_k, None, plain_text=text_to_set)
                            if open_k == (Path(self.current_file_path).resolve() if self.current_file_path else None):
                                self._plain_text_content = text_to_set
                                self.is_dirty = False
            except Exception as ex:
                self.logger.error("File I/O", f"Failed applying bulk delta: {ex}")
                # S5/S9b: Rollback applied files in reverse order to ensure all-or-nothing transaction safety
                for rolled_fp, is_bdl, prev_val, r_enc, r_bom, r_nl in reversed(applied_files):
                    try:
                        open_k = self._find_open_doc_key(rolled_fp)
                        if is_bdl:
                            self._restore_bundle_atomic(prev_val, rolled_fp)
                            if open_k and open_k in self.open_documents:
                                try:
                                    rb_doc, rb_env, rb_obj, _ = load_bundle_story(rolled_fp)
                                    old_env = self.open_documents[open_k].get("env")
                                    if old_env is not None and old_env is not rb_env:
                                        dispose_unity_env(old_env)
                                    self.open_documents[open_k]["doc"] = rb_doc
                                    self.open_documents[open_k]["env"] = rb_env
                                    self.open_documents[open_k]["obj"] = rb_obj
                                    self.open_documents[open_k]["dirty"] = False
                                    self._record_saved_checkpoint(open_k, rb_doc)
                                    if open_k == (Path(self.current_file_path).resolve() if self.current_file_path else None):
                                        self.current_doc = rb_doc
                                        self.current_unity_env = rb_env
                                        self.current_text_obj = rb_obj
                                        self.is_dirty = False
                                except Exception:
                                    pass
                        else:
                            if r_bom or (r_nl and r_nl != "\n"):
                                write_atomic_utf8(rolled_fp, prev_val, encoding=r_enc, has_bom=r_bom, newline=r_nl)
                            else:
                                write_atomic_utf8(rolled_fp, prev_val, encoding=r_enc)
                            if open_k and open_k in self.open_documents:
                                self.open_documents[open_k]["plain_text"] = prev_val
                                self.open_documents[open_k]["dirty"] = False
                                self._record_saved_checkpoint(open_k, None, plain_text=prev_val)
                                if open_k == (Path(self.current_file_path).resolve() if self.current_file_path else None):
                                    self._plain_text_content = prev_val
                                    self.is_dirty = False
                    except Exception as rb_ex:
                        self.logger.critical("File I/O", f"Rollback failed for '{rolled_fp}': {rb_ex}")
                messagebox.showerror(
                    "Undo/Redo Error",
                    f"Failed applying bulk file changes:\n{ex}\n\nOperation was safely rolled back."
                )
                raise

            if self.current_file_path and self._find_open_doc_key(self.current_file_path) is not None:
                self.open_file(self.current_file_path, reload_from_disk=True)

        if prev_caret:
            try:
                target_w = self._get_active_text_widget()
                if target_w and target_w.winfo_exists():
                    target_w.mark_set(tk.INSERT, prev_caret)
            except Exception:
                pass

    def _sync_edit_menu_states(self) -> None:
        """Dynamically update Undo/Redo labels and states in Edit menu."""
        if not hasattr(self, "edit_menu"):
            return
        try:
            cur_fp = str(self.current_file_path) if self.current_file_path else None
            can_u = self.undo_journal.can_undo(cur_fp)
            u_lbl = self.undo_journal.undo_label(cur_fp)
            self.edit_menu.entryconfigure(0, label=f"Undo {u_lbl}" if u_lbl else "Undo", state="normal" if can_u else "disabled")
            can_r = self.undo_journal.can_redo(cur_fp)
            r_lbl = self.undo_journal.redo_label(cur_fp)
            self.edit_menu.entryconfigure(1, label=f"Redo {r_lbl}" if r_lbl else "Redo", state="normal" if can_r else "disabled")
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Left Dock Tabs & Opened Files Cache Actions (#3B)
    # -------------------------------------------------------------------------
    def _switch_dock_tab(self, tab_name: str) -> None:
        """Switch left dock between Search Results and Opened Files."""
        self._left_dock_tab = tab_name
        t = self.theme
        active_fg = best_contrast_fg(t["misora_pink"])
        normal_fg = best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff")

        if tab_name == "files":
            self.tab_search_frame.pack_forget()
            self.tab_files_frame.pack(fill="both", expand=True)
            self.btn_tab_files.configure(bg=t["misora_pink"], fg=active_fg)
            self.btn_tab_search.configure(bg=t["bg_panel"], fg=normal_fg)
            self._refresh_opened_files_list()
        else:
            self.tab_files_frame.pack_forget()
            self.tab_search_frame.pack(fill="both", expand=True)
            self.btn_tab_search.configure(bg=t["misora_pink"], fg=active_fg)
            self.btn_tab_files.configure(bg=t["bg_panel"], fg=normal_fg)

    def _toggle_dock_collapse(self) -> None:
        """Toggle left dock between collapsed and expanded width strictly via h_paned."""
        if getattr(self, "_dock_collapsed", False):
            # Expand dock
            self._dock_collapsed = False
            target_w = getattr(self, "_left_dock_width", 340) or 340
            if hasattr(self, "btn_dock_pin") and self.btn_dock_pin.winfo_exists():
                self.btn_dock_pin.pack_forget()
            if hasattr(self, "btn_tab_search") and self.btn_tab_search.winfo_exists():
                self.btn_tab_search.pack(side="left", padx=(2, 2))
            if hasattr(self, "btn_tab_files") and self.btn_tab_files.winfo_exists():
                self.btn_tab_files.pack(side="left", padx=(2, 2))
            if hasattr(self, "btn_dock_pin") and self.btn_dock_pin.winfo_exists():
                self.btn_dock_pin.pack(side="right", padx=(2, 2))
                self.btn_dock_pin.configure(text="📌")
            if hasattr(self, "_dock_pin_tooltip"):
                self._dock_pin_tooltip.text = "Collapse Left Panel"
            if getattr(self, "_left_dock_tab", "search") == "files":
                if hasattr(self, "tab_files_frame") and not self.tab_files_frame.winfo_ismapped():
                    self.tab_files_frame.pack(fill="both", expand=True)
            else:
                if hasattr(self, "tab_search_frame") and not self.tab_search_frame.winfo_ismapped():
                    self.tab_search_frame.pack(fill="both", expand=True)
            self.h_paned.paneconfigure(self.left_frame, minsize=160)
            self.h_paned.sash_place(0, target_w, 0)
        else:
            # Collapse dock
            current_w = self.left_frame.winfo_width()
            if current_w >= 100:
                self._left_dock_width = current_w
            self._dock_collapsed = True
            if hasattr(self, "btn_tab_search") and self.btn_tab_search.winfo_exists():
                self.btn_tab_search.pack_forget()
            if hasattr(self, "btn_tab_files") and self.btn_tab_files.winfo_exists():
                self.btn_tab_files.pack_forget()
            if hasattr(self, "tab_search_frame") and self.tab_search_frame.winfo_ismapped():
                self.tab_search_frame.pack_forget()
            if hasattr(self, "tab_files_frame") and self.tab_files_frame.winfo_ismapped():
                self.tab_files_frame.pack_forget()
            if hasattr(self, "btn_dock_pin") and self.btn_dock_pin.winfo_exists():
                self.btn_dock_pin.pack_forget()
                self.btn_dock_pin.pack(side="left", padx=2, pady=2)
                self.btn_dock_pin.configure(text="▶")
            if hasattr(self, "_dock_pin_tooltip"):
                self._dock_pin_tooltip.text = "Expand Left Panel"
            self.h_paned.paneconfigure(self.left_frame, minsize=0)
            self.h_paned.sash_place(0, 36, 0)

    def _refresh_opened_files_list(self) -> None:
        """Re-render the list of cached opened files in the Opened Files dock tab."""
        if not hasattr(self, "txt_opened_files"):
            return
        self.txt_opened_files.config(state="normal")
        self.txt_opened_files.delete("1.0", tk.END)
        self._opened_files_line_map: Dict[int, Path] = {}

        count = len(self.open_documents)
        self.lbl_files_title.config(text=f"Opened Files ({count})")

        for idx, (fpath, info) in enumerate(self.open_documents.items(), start=1):
            line_no = idx
            self._opened_files_line_map[line_no] = fpath
            is_active = (fpath == self.current_file_path)
            is_dirty = bool(info.get("dirty", False))

            prefix = "● " if is_active else "  "
            dirty_mark = "* " if is_dirty else "  "
            tag_name = "file_active" if is_active else ("file_dirty" if is_dirty else "file_normal")

            self.txt_opened_files.insert(tk.END, prefix, ("file_close",))
            self.txt_opened_files.insert(tk.END, dirty_mark, ("file_dirty" if is_dirty else "file_dim",))
            self.txt_opened_files.insert(tk.END, fpath.name, (tag_name,))

            boxes = info.get("boxes_count", 0)
            detail = f" ({boxes} boxes)" if boxes else f" ({fpath.suffix})"
            self.txt_opened_files.insert(tk.END, detail, ("file_dim",))
            self.txt_opened_files.insert(tk.END, "  [×]\n", ("file_close",))

        self.txt_opened_files.config(state="disabled")

    def _on_opened_files_click(self, event: tk.Event) -> str:
        """Clicking an opened file switches to it; clicking [×] closes it."""
        idx_str = self.txt_opened_files.index(f"@{event.x},{event.y}")
        line_no = int(idx_str.split(".")[0])
        col_no = int(idx_str.split(".")[1])
        fpath = getattr(self, "_opened_files_line_map", {}).get(line_no)
        if not fpath:
            return "break"

        line_text = self.txt_opened_files.get(f"{line_no}.0", f"{line_no}.end")
        if "[×]" in line_text and col_no >= line_text.rfind("[×]"):
            self.close_file(fpath)
        else:
            if fpath != self.current_file_path:
                self.open_file(fpath)
        return "break"

    def close_file(self, file_path: Path) -> bool:
        """Close an opened file from in-memory cache, prompting if dirty (S3).

        Returns True if the file was closed, False if close was cancelled or aborted.
        """
        file_path = Path(file_path).resolve()
        if file_path == self.current_file_path:
            if not self._flush_active_widget():
                return False

        info = self.open_documents.get(file_path)
        is_dirty = (file_path == self.current_file_path and self.is_dirty) or (info and info.get("dirty", False))

        if is_dirty:
            ans = messagebox.askyesnocancel(
                "Unsaved Changes",
                f"'{file_path.name}' has unsaved changes.\nSave before closing?",
                parent=self,
            )
            if ans is None:
                return False
            if ans:
                if not self._save_document_entry(file_path):
                    return False

        closed_env = None
        if file_path in self.open_documents:
            closed_env = self.open_documents[file_path].get("env") if isinstance(self.open_documents[file_path], dict) else None
            del self.open_documents[file_path]
            self.undo_journal.prune_file(str(file_path))
            if closed_env is not None:
                dispose_unity_env(closed_env)

        self._saved_state_checkpoints.pop(str(file_path), None)

        if file_path == self.current_file_path:
            if self.current_unity_env is not None and (self.current_unity_env is closed_env or not self.open_documents):
                dispose_unity_env(self.current_unity_env)
                self.current_unity_env = None
                self.current_text_obj = None
            if self.open_documents:
                next_file = next(iter(self.open_documents))
                self.open_file(next_file)
            else:
                self.current_file_path = None
                self.current_doc = None
                self.current_unity_env = None
                self.current_text_obj = None
                self.is_bundle_file = False
                self.is_dirty = False
                self._plain_text_content = ""
                self._clear_card_registry()  # S4: prune stale card refs before view reset
                if hasattr(self, "undo_journal") and hasattr(self.undo_journal, "set_active_file"):
                    self.undo_journal.set_active_file("")
                self._update_views()
                self._sync_edit_menu_states()
                self.lbl_status.config(text="Ready. No files open.")

        self._refresh_opened_files_list()
        return True

    def close_others(self, keep_path: Path) -> None:
        """Close all opened files except keep_path."""
        keep_path = Path(keep_path).resolve()
        to_close = [p for p in list(self.open_documents.keys()) if p != keep_path]
        for p in to_close:
            if not self.close_file(p):
                break

    def close_all_unmodified(self) -> None:
        """Close all opened files that do not have unsaved changes."""
        to_close = []
        for p, info in list(self.open_documents.items()):
            is_dirty = (p == self.current_file_path and self.is_dirty) or info.get("dirty", False)
            if not is_dirty:
                to_close.append(p)
        for p in to_close:
            if not self.close_file(p):
                break

    def close_all_files(self) -> None:
        """Close all opened files, prompting on any unsaved changes."""
        for p in list(self.open_documents.keys()):
            if not self.close_file(p):
                break

    def _close_all_documents_without_prompt(self) -> None:
        """Close all open documents cleanly without prompting (used after ProjectDiffDialog confirmation)."""
        for p, info in list(self.open_documents.items()):
            env = info.get("env") if isinstance(info, dict) else None
            if env is not None:
                dispose_unity_env(env)
            if hasattr(self, "undo_journal"):
                self.undo_journal.prune_file(str(p))
            if hasattr(self, "_saved_state_checkpoints"):
                self._saved_state_checkpoints.pop(str(p), None)
        self.open_documents.clear()
        if self.current_unity_env is not None:
            dispose_unity_env(self.current_unity_env)
        self.current_file_path = None
        self.current_doc = None
        self.current_unity_env = None
        self.current_text_obj = None
        self.is_bundle_file = False
        self.is_dirty = False
        self._plain_text_content = ""
        self._locked_boxes = set()
        self._locked_box_uids = set()
        self._modified_boxes = set()
        self._modified_box_uids = set()
        self._original_box_texts = {}
        self._original_jp_by_uid = {}
        self._clear_card_registry()
        if hasattr(self, "undo_journal") and hasattr(self.undo_journal, "set_active_file"):
            self.undo_journal.set_active_file("")

    def on_save_project(self) -> None:
        """Prompt for a .misora file path and save the current workspace session."""
        if not self.open_documents:
            messagebox.showinfo("Save Project", "No files are currently open to save in a project.", parent=self)
            return
        init_dir = str(self.last_opened_dir) if getattr(self, "last_opened_dir", None) and self.last_opened_dir.exists() else None
        target = filedialog.asksaveasfilename(
            initialdir=init_dir,
            title="Save Misora Project",
            defaultextension=MISORA_WORKSPACE_EXT,
            filetypes=[("Misora Project", f"*{MISORA_WORKSPACE_EXT}"), ("All Files", "*.*")],
        )
        if target:
            self.save_project(Path(target))

    def save_project(self, workspace_path: Union[str, Path]) -> bool:
        """Save .misora v1 workspace session (strictly refs + state + stable locks ONLY)."""
        if not self._flush_active_widget():
            return False
        self._save_active_document_state()
        self._exit_raw_edit_mode(refresh=False)

        ws_path = Path(workspace_path).resolve()
        ws_dir = ws_path.parent

        file_entries: List[WorkspaceFileEntry] = []
        for raw_p, entry in self.open_documents.items():
            p = Path(raw_p).resolve()
            rel = safe_relpath(p, ws_dir)
            doc = entry.get("doc") if isinstance(entry, dict) else None
            locked_uids = set(entry.get("locked_box_uids", set())) if isinstance(entry, dict) else set()
            orig_jp_by_uid = dict(entry.get("original_jp_by_uid", {})) if isinstance(entry, dict) else {}
            stable_pairs = get_document_stable_locks(doc, locked_uids, orig_jp_by_uid)
            locked_keys = [LockedKeyEntry(box_ordinal=o, jp_sha256=h) for o, h in stable_pairs]
            file_entries.append(WorkspaceFileEntry(rel_path=rel, abs_path=str(p), locked_keys=locked_keys))

        active_file_str: Optional[str] = None
        if self.current_file_path is not None:
            cur_p = Path(self.current_file_path).resolve()
            rel_active = safe_relpath(cur_p, ws_dir)
            active_file_str = rel_active if rel_active else str(cur_p)

        view_mode = "continuous" if getattr(self, "var_continuous_view", None) and self.var_continuous_view.get() else "dialogue"
        search_scope = self.scope_var.get() if hasattr(self, "scope_var") else "project"

        session = WorkspaceSession(
            files=file_entries,
            active_file=active_file_str,
            active_box_idx=int(getattr(self, "current_box_idx", 0)),
            is_box0_active=bool(getattr(self, "is_box0_active", False)),
            view_mode=view_mode,
            search_scope=search_scope,
        )
        try:
            save_workspace(ws_path, session)
        except Exception as exc:
            self.logger.exception(f"Failed to save project '{ws_path.name}':", exc)
            messagebox.showerror("Save Project Error", f"Could not save project '{ws_path.name}':\n{exc}", parent=self)
            return False

        self.lbl_status.config(text=f"Saved project '{ws_path.name}' ({len(file_entries)} file(s)).")
        self.show_toast(f"Saved project: {ws_path.name}")
        return True

    def on_open_project(self) -> None:
        """Prompt for a .misora file and open the workspace session."""
        init_dir = str(self.last_opened_dir) if getattr(self, "last_opened_dir", None) and self.last_opened_dir.exists() else None
        target = filedialog.askopenfilename(
            initialdir=init_dir,
            title="Open Misora Project",
            filetypes=[("Misora Project", f"*{MISORA_WORKSPACE_EXT}"), ("All Files", "*.*")],
        )
        if target:
            self.open_project(Path(target))

    def open_project(self, workspace_path: Union[str, Path]) -> bool:
        """Open a .misora v1 workspace session with U-B18 diff dialog and stable lock matching."""
        ws_path = Path(workspace_path).resolve()
        ws_dir = ws_path.parent
        try:
            session = load_workspace(ws_path)
        except (WorkspaceError, UnicodeDecodeError, OSError) as exc:
            self.logger.error("Workspace", f"Failed to load '{ws_path}': {exc}")
            messagebox.showerror("Open Project Error", f"Could not open project '{ws_path.name}':\n{exc}", parent=self)
            return False

        resolved_entries: List[Tuple[WorkspaceFileEntry, Optional[Path]]] = []
        missing_labels: List[str] = []
        for entry in session.files:
            resolved = resolve_workspace_file_path(ws_dir, entry.rel_path, entry.abs_path)
            resolved_entries.append((entry, resolved))
            if resolved is None:
                missing_labels.append(entry.rel_path or entry.abs_path)

        target_paths = [resolved for _, resolved in resolved_entries if resolved is not None]

        # Safeguard 3: Flush active widget & save active state BEFORE computing diff
        if self.open_documents:
            if not self._flush_active_widget():
                return False
            self._save_active_document_state()
            diff_entries = compute_workspace_diff(
                self.open_documents,
                target_paths,
                current_file_path=self.current_file_path,
                current_is_dirty=getattr(self, "is_dirty", False),
            )
            dlg = ProjectDiffDialog(self, diff_entries, ws_path.name)
            choice = getattr(dlg, "result", "cancel")
            if choice == "cancel":
                return False
            if choice == "save":
                for p in list(self.open_documents.keys()):
                    info = self.open_documents.get(p, {})
                    is_doc_dirty = (p == self.current_file_path and getattr(self, "is_dirty", False)) or bool(
                        info.get("dirty", False) if isinstance(info, dict) else False
                    )
                    if is_doc_dirty and not self._save_document_entry(p):
                        return False

        self._close_all_documents_without_prompt()

        unresolved_notices: List[str] = []
        opened_entries: List[Tuple[WorkspaceFileEntry, Path]] = []
        for entry, resolved in resolved_entries:
            if resolved is None:
                continue
            try:
                self.open_file(resolved, refresh_ui=False)
            except Exception as exc:
                self.logger.error("Workspace", f"Failed opening '{resolved}': {exc}")
                missing_labels.append(str(resolved))
                continue

            doc_key = self._find_open_doc_key(resolved)
            if doc_key is not None and doc_key in self.open_documents:
                opened_entries.append((entry, doc_key))
                doc_entry = self.open_documents[doc_key]
                doc = doc_entry.get("doc")
                orig_map = doc_entry.get("original_jp_by_uid", {})
                stable_pairs = [(lk.box_ordinal, lk.jp_sha256) for lk in entry.locked_keys]
                if stable_pairs:
                    matched_uids, unresolved = restore_stable_locks(doc, stable_pairs, orig_map)
                    doc_entry["locked_box_uids"] = set(matched_uids)
                    if doc_key == self.current_file_path:
                        self._locked_box_uids = set(matched_uids)
                        self._resync_box_indices_from_uids()
                    if unresolved:
                        unresolved_notices.append(
                            f"{doc_key.name}: {len(unresolved)} lock(s) unresolved"
                        )

        # Restore view_mode & search_scope (Safeguard 4)
        if hasattr(self, "var_continuous_view"):
            self.var_continuous_view.set(session.view_mode == "continuous")
        if hasattr(self, "scope_var"):
            self.scope_var.set(session.search_scope)

        # Safeguard 3: All files missing grace -> restore empty state cleanly
        if not opened_entries:
            self._update_top_header_title()
            self._sync_scope_widgets()
            self._update_views()
            self._refresh_opened_files_list()
            self._dirty_state_changed()
            self._sync_edit_menu_states()
            if missing_labels:
                msg = f"All {len(missing_labels)} file(s) referenced by '{ws_path.name}' were not found on disk."
                self.logger.warning("Workspace", msg)
                messagebox.showwarning("Missing Project Files", msg, parent=self)
                self.lbl_status.config(text=msg)
            return True

        # Safeguard 1 & 2: Match active_file against rel_path & abs_path, then apply cursor AFTER activation
        target_active = match_active_file(session.active_file, ws_dir, resolved_entries)
        if target_active is None:
            target_active = opened_entries[0][1]
        self.open_file(target_active, refresh_ui=False)

        if self.current_doc and self.current_doc.boxes:
            self.current_box_idx = max(0, min(session.active_box_idx, len(self.current_doc.boxes) - 1))
        else:
            self.current_box_idx = 0
        self.is_box0_active = bool(session.is_box0_active)

        active_key = self._find_open_doc_key(target_active)
        if active_key is not None and active_key in self.open_documents:
            self._locked_box_uids = set(self.open_documents[active_key].get("locked_box_uids", set()))
            self._resync_box_indices_from_uids()

        # Safeguard 4: Sync view, header title, and scope UI controls together
        self._update_top_header_title()
        self._sync_scope_widgets()
        self._update_views()
        self._refresh_opened_files_list()
        self._dirty_state_changed()
        self._sync_edit_menu_states()

        notices: List[str] = []
        if missing_labels:
            notices.append(f"Missing file(s) skipped ({len(missing_labels)}): " + ", ".join(missing_labels[:5]))
        if unresolved_notices:
            notices.append("Unresolved Translation Locks (not transferred): " + "; ".join(unresolved_notices))
        if notices:
            full_notice = "\n".join(notices)
            self.logger.warning("Workspace", full_notice)
            messagebox.showwarning("Project Open Notice", full_notice, parent=self)

        self.lbl_status.config(text=f"Opened project '{ws_path.name}' ({len(opened_entries)} file(s)).")
        return True

    # -------------------------------------------------------------------------
    # Right-Click Context Menus & External Editor Launching (#4D)
    # -------------------------------------------------------------------------
    def _on_results_right_click(self, event: tk.Event) -> str:
        """Right-click in search results shows file actions context menu."""
        idx_str = self.txt_results.index(f"@{event.x},{event.y}")
        line_no = int(idx_str.split(".")[0])
        entry = self._result_line_map.get(line_no)
        target_path: Optional[Path] = None
        if entry:
            kind, payload = entry
            if kind == "header":
                target_path = Path(payload)
            elif kind == "item":
                res_idx = int(payload)
                if 0 <= res_idx < len(self.active_search_results):
                    target_path = self.active_search_results[res_idx].file_path
        if target_path and target_path.exists():
            self._show_file_context_menu(event, target_path)
        return "break"

    def _on_opened_files_right_click(self, event: tk.Event) -> str:
        """Right-click in opened files list shows file actions context menu."""
        idx_str = self.txt_opened_files.index(f"@{event.x},{event.y}")
        line_no = int(idx_str.split(".")[0])
        fpath = getattr(self, "_opened_files_line_map", {}).get(line_no)
        if fpath and fpath.exists():
            self._show_file_context_menu(event, fpath)
        return "break"

    def _show_file_context_menu(self, event: tk.Event, target_path: Path) -> None:
        """Show right-click context menu with Close, Close Others, Reveal in Explorer, etc."""
        t = self.theme
        panel_fg = best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff")
        accent_fg = best_contrast_fg(t["misora_pink"])

        menu = tk.Menu(self, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg)

        menu.add_command(label=f"Switch to '{target_path.name}'", command=lambda: self.open_file(target_path))
        if target_path in self.open_documents:
            menu.add_command(label="Close File", command=lambda: self.close_file(target_path))
            menu.add_command(label="Close Others", command=lambda: self.close_others(target_path))
            menu.add_command(label="Close All Unmodified", command=self.close_all_unmodified)
            menu.add_command(label="Close All", command=self.close_all_files)
            menu.add_separator()
            if target_path == self.current_file_path:
                menu.add_command(label="Save File (Ctrl+S)", command=self.on_save)

        menu.add_separator()
        menu.add_command(label="Reveal in File Explorer", command=lambda: self._open_containing_folder(target_path))

        open_with = tk.Menu(menu, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg)
        open_with.add_command(label="Notepad", command=lambda: self._launch_editor_on_file("notepad.exe", target_path))
        if self.notepadpp_path and Path(self.notepadpp_path).exists():
            open_with.add_command(label="Notepad++", command=lambda: self._launch_editor_on_file(str(self.notepadpp_path), target_path))
        if self.external_editor_path and Path(self.external_editor_path).exists():

