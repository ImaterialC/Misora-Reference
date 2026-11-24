# ======================================================================
# FILE: misora.py — PART 08 / 10
# ORIGINAL LINE RANGE : L9397 .. L10873 (total 1477 lines of 12835)
# SOURCE SHA-256      : d23baae2be82fe93a18da7d3769af30d19ebe02a8b5f6a3645d56a6f53c0710e
# NOTE FOR AI REVIEWER: Cite ORIGINAL line numbers (L9397..L10873) and symbol names.
# SYMBOLS IN THIS PART (with exact original line numbers):
#   L09397:   MisoraApp._render_search_results (def)
#   L09460:   MisoraApp._on_results_click (def)
#   L09479:   MisoraApp._on_results_step (def)
#   L09492:   MisoraApp._select_result_index (def)
#   L09579:   MisoraApp.on_clear_search (def)
#   L09590:   MisoraApp._sync_recent_files_menu (def)
#   L09611:   MisoraApp._clear_recent_files (def)
#   L09616:   MisoraApp.on_open_file (def)
#   L09633:   MisoraApp.on_open_folder (def)
#   L09642:   MisoraApp._get_project_display_path (def)
#   L09658:   MisoraApp._on_folder_path_var_trace (def)
#   L09675:   MisoraApp._sync_scope_widgets (def)
#   L09706:   MisoraApp.on_browse_scope_path (def)
#   L09714:   MisoraApp.on_browse_project_folder (def)
#   L09729:   MisoraApp.on_show_find (def)
#   L09741:   MisoraApp.on_show_find_in_files (def)
#   L09745:   MisoraApp.on_show_replace (def)
#   L09760:   MisoraApp._hide_search_bar (def)
#   L09767:   MisoraApp.on_replace_next (def)
#   L09855:   MisoraApp.on_replace_all (def)
#   L10100:   MisoraApp.on_undo (def)
#   L10118:   MisoraApp.on_redo (def)
#   L10136:   MisoraApp._restore_bundle_atomic (def)
#   L10167:   MisoraApp._apply_delta (def)
#   L10363:   MisoraApp._sync_edit_menu_states (def)
#   L10381:   MisoraApp._switch_dock_tab (def)
#   L10400:   MisoraApp._toggle_dock_collapse (def)
#   L10425:   MisoraApp._refresh_opened_files_list (def)
#   L10457:   MisoraApp._on_opened_files_click (def)
#   L10474:   MisoraApp.close_file (def)
#   L10535:   MisoraApp.close_others (def)
#   L10543:   MisoraApp.close_all_unmodified (def)
#   L10554:   MisoraApp.close_all_files (def)
#   L10563:   MisoraApp._on_results_right_click (def)
#   L10581:   MisoraApp._on_opened_files_right_click (def)
#   L10590:   MisoraApp._show_file_context_menu (def)
#   L10630:   MisoraApp._open_containing_folder (def)
#   L10640:   MisoraApp._launch_editor_on_file (def)
#   L10656:   MisoraApp._choose_app_and_open (def)
#   L10662:   MisoraApp._copy_to_clipboard (def)
#   L10667:   MisoraApp._sync_external_editor_menu (def)
#   L10677:   MisoraApp.on_set_external_editor (def)
#   L10688:   MisoraApp.on_clear_external_editor (def)
#   L10696:   MisoraApp.on_launch_datamine (def)
#   L10766:   MisoraApp.on_select_datamine_exe (def)
#   L10782:   MisoraApp.on_open_datamine_folder (def)
#   L10791:   MisoraApp.on_open_backups_folder (def)
#   L10795:   MisoraApp.on_open_project_folder (def)
#   L10808:   MisoraApp.on_open_bepinex_folder (def)
#   L10812:   MisoraApp.on_open_program_folder (def)
#   L10815:   MisoraApp.on_open_xuat_text_folder (def)
#   L10845:   MisoraApp.on_open_redirected_resources_folder (def)
#   L10867:   MisoraApp.on_open_selected_search_folder (def)
# ======================================================================

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
        f = filedialog.askopenfilename(
            initialdir=init_dir,
            title="Open Story Asset or Script",
            filetypes=[
                ("Priconne Assets & Scripts", "*.unity3d;*.asset;*.txt;*.json"),
                ("Unity3D Bundles", "*.unity3d;*.asset"),
                ("Text Scripts", "*.txt;*.json"),
                ("All Files", "*.*")
            ]
        )
        if f:
            self.last_opened_dir = Path(f).parent
            self.open_file(f)
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
                self.folder_path_entry.config(state="normal")
                self.btn_browse_search_folder.config(state="normal")
                if getattr(self, "selected_search_folder", None):
                    self.folder_path_var.set(str(self.selected_search_folder))
                else:
                    self.folder_path_var.set("")
            elif scope == "project":
                self.folder_path_entry.config(state="normal")
                self.btn_browse_search_folder.config(state="normal")
                self.folder_path_var.set(self._get_project_display_path())
            else:  # "current"
                if getattr(self, "current_file_path", None):
                    self.folder_path_var.set(str(self.current_file_path.parent))
                elif getattr(self, "open_documents", None) and self.open_documents:
                    first_path = next(iter(self.open_documents.keys()))
                    self.folder_path_var.set(str(first_path.parent) if isinstance(first_path, Path) else "(Current Open Files)")
                else:
                    self.folder_path_var.set("(Current Open Files)")
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
            self.row_replace.pack_forget()
            self._replace_row_visible = False
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)

    def on_show_find_in_files(self) -> None:
        self.scope_var.set("project")
        self.on_show_find()

    def on_show_replace(self) -> None:
        if not getattr(self, "_search_bar_visible", False):
            self.search_frame.pack(before=self.h_paned, fill="x", padx=8, pady=(6, 4))
            self._search_bar_visible = True
        if not getattr(self, "_replace_row_visible", False):
            children = self.search_frame.winfo_children()
            row1 = children[0] if children else None
            if row1:
                self.row_replace.pack(fill="x", padx=8, pady=(0, 4), after=row1)
            else:
                self.row_replace.pack(fill="x", padx=8, pady=(0, 4))
            self._replace_row_visible = True
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)

    def _hide_search_bar(self) -> None:
        if hasattr(self, "search_frame"):
            self.search_frame.pack_forget()
            self._search_bar_visible = False
            target = self.txt_continuous if self.var_continuous_view.get() else self.txt_dialogue
            target.focus_set()

    def on_replace_next(self) -> None:
        """Find and replace the next occurrence in the active file."""
        find_text = self.search_var.get()
        replace_text = self.replace_var.get()
        if not find_text:
            return

        if not self.current_file_path:
            messagebox.showinfo("Replace", "No active file open to replace in.")
            return

        if self.current_doc and self.current_doc.boxes:
            box = self.current_doc.boxes[self.current_box_idx]
            if find_text in box.clean_text:
                if self.is_box_locked(self.current_box_idx):
                    self.show_toast(f"🔒 Box {self.current_box_idx + 1} is locked against edits.")
                else:
                    old_sp = box.speaker
                    old_tx = box.clean_text
                    box_uid = box.uid
                    old_segs = [s.text for s in box.segs] if len(box.segs) > 1 else None
                    new_tx = box.clean_text.replace(find_text, replace_text, 1)
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
                if find_text in self.current_doc.boxes[next_idx].clean_text:
                    self.current_box_idx = next_idx
                    self._update_views()
                    self.lbl_status.config(text=f"Found match in Box #{next_idx + 1}. Press Replace again to replace.")
                    return
            messagebox.showinfo("Replace", f"No more occurrences of '{find_text}' found.")
        elif not self.current_doc and self.current_file_path:
            cur_tx = self._plain_text_content
            if find_text in cur_tx:
                new_tx = cur_tx.replace(find_text, replace_text, 1)
                self.undo_journal.record(
                    PlainTextDelta(
                        file_path=str(self.current_file_path),
                        old_content=cur_tx,
                        new_content=new_tx,
                    ),
                    label=f"Replace in {self.current_file_path.name}"
                )
                self._plain_text_content = new_tx
                if self.current_file_path and self.current_file_path in self.open_documents:
                    self.open_documents[self.current_file_path]["plain_text"] = new_tx
                self._mark_document_dirty(self.current_file_path)
                self._dirty_state_changed()
                self._update_views()
                self.lbl_status.config(text=f"Replaced 1 occurrence in {self.current_file_path.name}")
            else:
                messagebox.showinfo("Replace", f"'{find_text}' not found in current file.")

    def on_replace_all(self) -> None:
        """Replace all occurrences in current file or across project/folder."""
        find_text = self.search_var.get()
        replace_text = self.replace_var.get()
        if not find_text:
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
                    if find_text in box.clean_text:
                        if self.is_box_locked(idx):
                            skipped_locked += 1
                            continue
                        old_sp = box.speaker
                        old_tx = box.clean_text
                        new_tx = box.clean_text.replace(find_text, replace_text)
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
                if find_text in cur_tx:
                    occurrences = cur_tx.count(find_text)
                    new_tx = cur_tx.replace(find_text, replace_text)
                    self.undo_journal.record(
                        PlainTextDelta(
                            file_path=str(self.current_file_path),
                            old_content=cur_tx,
                            new_content=new_tx,
                        ),
                        label=f"Replace All in {self.current_file_path.name}"
                    )
                    self._plain_text_content = new_tx
                    if self.current_file_path and self.current_file_path in self.open_documents:
                        self.open_documents[self.current_file_path]["plain_text"] = new_tx
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

            inc_bdl = self.var_inc_bundles.get()
            inc_txt = self.var_inc_text.get()

            matching_files: Dict[Path, int] = {}
            total_matches = 0
            candidate_files: List[Path] = []
            for root in target_roots:
                if root.is_file():
                    candidate_files.append(root)
                elif root.is_dir():
                    if inc_bdl:
                        candidate_files.extend(root.rglob("*.unity3d"))
                        candidate_files.extend(root.rglob("*.asset"))
                    if inc_txt:
                        candidate_files.extend(root.rglob("*.txt"))

            for cf in candidate_files:
                try:
                    if cf.suffix.lower() in (".unity3d", ".asset"):
                        # Decode structured story TextAsset rather than scanning raw compressed bytes (S9b)
                        bundle_env = None
                        try:
                            b_doc, bundle_env, _, _ = load_bundle_story(cf)
                            c = 0
                            for box in b_doc.boxes:
                                if find_text in box.clean_text:
                                    c += box.clean_text.count(find_text)
                            if c > 0:
                                matching_files[cf] = c
                                total_matches += c
                        finally:
                            if bundle_env is not None:
                                dispose_unity_env(bundle_env)
                    else:
                        decoded = read_text_file_strictly(cf)
                        c = decoded.text.count(find_text)
                        if c > 0:
                            matching_files[cf] = c
                            total_matches += c
                except Exception:
                    pass

            if not matching_files:
                messagebox.showinfo("Replace All", f"No matches for '{find_text}' found across {len(candidate_files)} files.")
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
                            modified = False
                            for idx, box in enumerate(doc.boxes):
                                if find_text in box.clean_text:
                                    new_box_tx = box.clean_text.replace(find_text, replace_text)
                                    doc.inject_box(idx, None, new_box_tx)
                                    modified = True
                            if modified:
                                bak_dir = self._get_backup_dir()
                                ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                                orig_bak_path = bak_dir / f"{fpath.stem}.orig_{ts}{fpath.suffix}"
                                shutil.copy2(fpath, orig_bak_path)

                                save_bundle_story(bundle_env, obj, doc, fpath, backup_dir=bak_dir)

                                mod_bak_path = bak_dir / f"{fpath.stem}.mod_{ts}{fpath.suffix}"
                                shutil.copy2(fpath, mod_bak_path)

                                per_file_deltas.append((str(fpath), str(orig_bak_path), str(mod_bak_path), True))
                                replaced_files_count += 1
                                # S9b: Synchronize in-memory open_documents cache & checkpoint
                                f_res = fpath.resolve()
                                if f_res in self.open_documents:
                                    self._record_saved_checkpoint(f_res, doc)
                                    self._mark_document_dirty(f_res)
                        finally:
                            if bundle_env is not None:
                                dispose_unity_env(bundle_env)
                    else:
                        decoded = read_text_file_strictly(fpath)
                        old_txt = decoded.text
                        if find_text in old_txt:
                            new_txt = old_txt.replace(find_text, replace_text)
                            bak_dir = self._get_backup_dir()
                            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                            bak_path = bak_dir / f"{fpath.stem}.bak_{ts}{fpath.suffix}"
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
                            # S5: Synchronize in-memory open_documents cache & checkpoint
                            f_res = fpath.resolve()
                            if f_res in self.open_documents:
                                self.open_documents[f_res]["plain_text"] = new_txt
                                self.open_documents[f_res]["encoding"] = decoded.encoding
                                self.open_documents[f_res]["has_bom"] = decoded.has_bom
                                self.open_documents[f_res]["newline"] = decoded.newline
                                self._record_saved_checkpoint(f_res, None, plain_text=new_txt)
                                self._mark_document_dirty(f_res)
                except Exception as ex:
                    self.logger.error("Search", f"Failed replacing in {fpath}: {ex}")

            if per_file_deltas:
                self.undo_journal.record(
                    BulkFileDelta(
                        description=f"Replace '{find_text}' -> '{replace_text}' in {len(per_file_deltas)} files",
                        per_file=per_file_deltas,
                    )
                )

            if self.current_file_path and self.current_file_path in matching_files:
                self.open_file(self.current_file_path, reload_from_disk=True)

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

                        # S9b: Synchronize in-memory cache and checkpoints if open
                        if fp in self.open_documents:
                            try:
                                b_doc, b_env, b_obj, _ = load_bundle_story(fp)
                                old_env = self.open_documents[fp].get("bundle_env")
                                if old_env is not None and old_env is not b_env:
                                    dispose_unity_env(old_env)
                                self.open_documents[fp]["doc"] = b_doc
                                self.open_documents[fp]["bundle_env"] = b_env
                                self.open_documents[fp]["target_object"] = b_obj
                                self._record_saved_checkpoint(fp, b_doc)
                            except Exception:
                                pass
                            self._mark_document_dirty(fp)
                    else:
                        old_tx = item[1]
                        new_tx = item[2]
                        text_to_set = old_tx if reverse else new_tx
                        prev_text = new_tx if reverse else old_tx
                        doc_entry = self.open_documents.get(fp, {})
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

                        # S5: Synchronize in-memory cache and checkpoints if open
                        if fp in self.open_documents:
                            self.open_documents[fp]["plain_text"] = text_to_set
                            self._record_saved_checkpoint(fp, None, plain_text=text_to_set)
                            self._mark_document_dirty(fp)
            except Exception as ex:
                self.logger.error("File I/O", f"Failed applying bulk delta: {ex}")
                # S5/S9b: Rollback applied files in reverse order to ensure all-or-nothing transaction safety
                for rolled_fp, is_bdl, prev_val, r_enc, r_bom, r_nl in reversed(applied_files):
                    try:
                        if is_bdl:
                            self._restore_bundle_atomic(prev_val, rolled_fp)
                            if rolled_fp in self.open_documents:
                                try:
                                    rb_doc, rb_env, rb_obj, _ = load_bundle_story(rolled_fp)
                                    old_env = self.open_documents[rolled_fp].get("bundle_env")
                                    if old_env is not None and old_env is not rb_env:
                                        dispose_unity_env(old_env)
                                    self.open_documents[rolled_fp]["doc"] = rb_doc
                                    self.open_documents[rolled_fp]["bundle_env"] = rb_env
                                    self.open_documents[rolled_fp]["target_object"] = rb_obj
                                    self._record_saved_checkpoint(rolled_fp, rb_doc)
                                except Exception:
                                    pass
                        else:
                            if r_bom or (r_nl and r_nl != "\n"):
                                write_atomic_utf8(rolled_fp, prev_val, encoding=r_enc, has_bom=r_bom, newline=r_nl)
                            else:
                                write_atomic_utf8(rolled_fp, prev_val, encoding=r_enc)
                            if rolled_fp in self.open_documents:
                                self.open_documents[rolled_fp]["plain_text"] = prev_val
                                self._record_saved_checkpoint(rolled_fp, None, plain_text=prev_val)
                    except Exception as rb_ex:
                        self.logger.critical("File I/O", f"Rollback failed for '{rolled_fp}': {rb_ex}")
                messagebox.showerror(
                    "Undo/Redo Error",
                    f"Failed applying bulk file changes:\n{ex}\n\nOperation was safely rolled back."
                )
                raise

            if self.current_file_path:
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
        """Toggle left dock between collapsed and expanded width."""
        if getattr(self, "_dock_collapsed", False):
            # Expand dock
            self._dock_collapsed = False
            target_w = getattr(self, "_left_dock_width", 340) or 340
            self.h_paned.paneconfigure(self.left_frame, minsize=160)
            self.h_paned.sash_place(0, target_w, 0)
            if hasattr(self, "btn_dock_pin") and self.btn_dock_pin.winfo_exists():
                self.btn_dock_pin.configure(text="📌")
            if hasattr(self, "_dock_pin_tooltip"):
                self._dock_pin_tooltip.text = "Collapse Left Panel"
        else:
            # Collapse dock
            current_w = self.left_frame.winfo_width()
            if current_w >= 100:
                self._left_dock_width = current_w
            self._dock_collapsed = True
            self.h_paned.paneconfigure(self.left_frame, minsize=0)
            self.h_paned.sash_place(0, 36, 0)
            if hasattr(self, "btn_dock_pin") and self.btn_dock_pin.winfo_exists():
                self.btn_dock_pin.configure(text="◀")
            if hasattr(self, "_dock_pin_tooltip"):
                self._dock_pin_tooltip.text = "Expand Left Panel"

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
            open_with.add_command(label=f"Custom: {Path(self.external_editor_path).stem}", command=lambda: self._launch_editor_on_file(str(self.external_editor_path), target_path))
        open_with.add_separator()
        open_with.add_command(label="Choose another app...", command=lambda: self._choose_app_and_open(target_path))
        menu.add_cascade(label="Open With", menu=open_with)

        menu.add_separator()
        menu.add_command(label="Copy Full Path", command=lambda: self._copy_to_clipboard(str(target_path)))
        menu.add_command(label="Copy File Name", command=lambda: self._copy_to_clipboard(target_path.name))

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _open_containing_folder(self, target_path: Path) -> None:
        """Reveal file in Windows Explorer."""
        try:
            if target_path.exists():
                subprocess.Popen(["explorer.exe", f"/select,{target_path}"])
            else:
                subprocess.Popen(["explorer.exe", str(target_path.parent)])
        except Exception as e:
            self.logger.error("File I/O", f"Failed to reveal in explorer: {e}")

    def _launch_editor_on_file(self, exe: str, target_path: Path) -> None:
        """Launch an external editor on target_path, warning if unsaved in Misora."""
        if target_path == self.current_file_path and self.is_dirty:
            warn = messagebox.askokcancel(
                "Unsaved Changes",
                f"'{target_path.name}' has unsaved changes in Misora.\nOpening in an external editor will show the version currently on disk.\nContinue?"
            )
            if not warn:
                return
        try:
            subprocess.Popen([exe, str(target_path)], shell=False)
            self.logger.info("External Tools", f"Opened {target_path.name} in {exe}")
        except Exception as ex:
            self.logger.exception(f"Failed to launch {exe}:", ex)
            messagebox.showerror("Launch Error", f"Failed to launch external editor:\n{ex}")

    def _choose_app_and_open(self, target_path: Path) -> None:
        """One-time browse for application to open file."""
        app = filedialog.askopenfilename(title="Choose Application to Open File", filetypes=[("Executables", "*.exe;*.bat;*.cmd"), ("All Files", "*.*")])
        if app:
            self._launch_editor_on_file(app, target_path)

    def _copy_to_clipboard(self, text: str) -> None:
        self.clipboard_clear()
        self.clipboard_append(text)
        self.lbl_status.config(text=f"Copied to clipboard: {text}")

    def _sync_external_editor_menu(self) -> None:
        if not hasattr(self, "_ext_editor_menu"):
            return
        self._ext_editor_menu.delete(0, "end")
        self._ext_editor_menu.add_command(label="Set / Change Editor Program...", command=self.on_set_external_editor)
        self._ext_editor_menu.add_command(label="Clear Editor Selection", command=self.on_clear_external_editor)
        self._ext_editor_menu.add_separator()
        cur_desc = f"Current: {self.external_editor_path.name}" if self.external_editor_path else "Current: (None - default)"
        self._ext_editor_menu.add_command(label=cur_desc, state="disabled")

    def on_set_external_editor(self) -> None:
        f = filedialog.askopenfilename(
            title="Select External Text Editor Executable",
            filetypes=[("Executables", "*.exe;*.bat;*.cmd"), ("All Files", "*.*")]
        )
        if f:
            self.external_editor_path = Path(f)
            self._save_user_prefs(silent=True)
            self.lbl_status.config(text=f"External editor set to: {self.external_editor_path.name}")
            self.logger.info("External Tools", f"Configured external editor: {self.external_editor_path}")

    def on_clear_external_editor(self) -> None:
        self.external_editor_path = None
        self._save_user_prefs(silent=True)
        self.lbl_status.config(text="External editor selection cleared.")

    # -------------------------------------------------------------------------
    # Datamine Tool Launcher (#4C)
    # -------------------------------------------------------------------------
    def on_launch_datamine(self) -> None:
        """Launch the external Datamine executable or Python script with confirmation."""
        if not self.datamine_exe or not Path(self.datamine_exe).exists():
            ans = messagebox.askyesno("Datamine Tool Not Set", "No datamine executable has been configured yet.\nWould you like to select one now?")
            if ans:
                self.on_select_datamine_exe()
            return

        exe_path = Path(self.datamine_exe)
        if not self._datamine_confirm_skip:
            dlg = tk.Toplevel(self)
            dlg.title("Confirm Datamine Launch")
            dlg.geometry("440x180")
            dlg.transient(self)
            dlg.grab_set()
            dlg.resizable(False, False)
            t = self.theme
            dlg.configure(bg=t["bg_panel"])

            confirmed = [False]
            skip_var = tk.BooleanVar(master=dlg, value=False)

            msg = f"Launch external datamine tool?\n\nProgram: {exe_path.name}\nPath: {exe_path}"
            tk.Label(dlg, text=msg, bg=t["bg_panel"], fg=best_contrast_fg(t["bg_panel"]), justify="left", wraplength=400).pack(padx=16, pady=(16, 8), fill="x")

            cb = tk.Checkbutton(dlg, text="Don't ask again this session", variable=skip_var, bg=t["bg_panel"], fg=best_contrast_fg(t["bg_panel"]), selectcolor=t["bg_dark"])
            cb.pack(padx=16, pady=4, anchor="w")

            btn_frame = tk.Frame(dlg, bg=t["bg_panel"])
            btn_frame.pack(fill="x", padx=16, pady=(8, 12), side="bottom")

            def _cancel(_e: Optional[tk.Event] = None) -> None:
                safe_grab_release(dlg)
                if dlg.winfo_exists():
                    dlg.destroy()

            def _ok() -> None:
                confirmed[0] = True
                if skip_var.get():
                    self._datamine_confirm_skip = True
                safe_grab_release(dlg)
                if dlg.winfo_exists():
                    dlg.destroy()

            dlg.protocol("WM_DELETE_WINDOW", _cancel)
            dlg.bind("<Escape>", _cancel)

            btn_cancel = ttk.Button(btn_frame, text="Cancel", style="TButton", command=_cancel)
            btn_cancel.pack(side="right", padx=4)
            btn_ok = ttk.Button(btn_frame, text="Launch Tool", style="Pink.TButton", command=_ok)
            btn_ok.pack(side="right", padx=4)
            btn_cancel.focus_set()

            self.wait_window(dlg)
            if not confirmed[0]:
                return

        try:
            cwd = str(exe_path.parent)
            if exe_path.suffix.lower() == ".py":
                cmd = [sys.executable, str(exe_path)]
            else:
                cmd = [str(exe_path)]
            subprocess.Popen(cmd, cwd=cwd, shell=False)
            self.logger.info("External Tools", f"Launched datamine tool: {exe_path}")
            self.lbl_status.config(text=f"Launched datamine tool: {exe_path.name}")
        except Exception as exc:
            self.logger.exception("Failed to launch datamine tool:", exc)
            messagebox.showerror("Datamine Launch Failed", f"Could not launch {exe_path.name}:\n{exc}")

    def on_select_datamine_exe(self) -> None:
        f = filedialog.askopenfilename(
            title="Select Datamine Executable or Script",
            filetypes=[
                ("Executables & Scripts", "*.exe;*.py;*.bat;*.cmd"),
                ("Applications", "*.exe"),
                ("Python Scripts", "*.py"),
                ("All Files", "*.*")
            ]
        )
        if f:
            self.datamine_exe = Path(f)
            self._save_user_prefs(silent=True)
            self.lbl_status.config(text=f"Datamine tool set to: {self.datamine_exe.name}")
            self.logger.info("External Tools", f"Configured datamine executable: {self.datamine_exe}")

    def on_open_datamine_folder(self) -> None:
        if self.datamine_exe and Path(self.datamine_exe).exists():
            subprocess.Popen(["explorer.exe", str(Path(self.datamine_exe).parent)])
        else:
            messagebox.showinfo("Datamine Folder", "No datamine executable is currently configured.")

    # -------------------------------------------------------------------------
    # Folders & Files Configuration Dialog (#4B)
    # -------------------------------------------------------------------------
    def on_open_backups_folder(self) -> None:
        bak_dir = self._get_backup_dir()
        subprocess.Popen(["explorer.exe", str(bak_dir)])

    def on_open_project_folder(self) -> None:
        """Open the Project Root / Mod Translation directory in Windows Explorer."""
        p = getattr(self, "project_folder", None) or getattr(self, "bepinex_project_folder", None)
        if not p or not Path(p).exists():
            if getattr(self, "xuat_search_roots", None) and self.xuat_search_roots:
                p = self.xuat_search_roots[0]
        if p and Path(p).exists():
            subprocess.Popen(["explorer.exe", str(p)])
        else:
            ans = messagebox.askyesno("Project Folder", "Project / Mod translation folder is not set. Configure it now?")
            if ans:
                self.on_open_paths_dialog()

    def on_open_bepinex_folder(self) -> None:
        """Backward-compatible alias for on_open_project_folder."""
        self.on_open_project_folder()

    def on_open_program_folder(self) -> None:
        subprocess.Popen(["explorer.exe", str(SCRIPT_DIR)])

    def on_open_xuat_text_folder(self) -> None:
        """Open the Text translation directory in Windows Explorer (supports XUAT, MelonLoader, BepInEx)."""
        p: Optional[Path] = None
        proj = getattr(self, "project_folder", None) or getattr(self, "bepinex_project_folder", None)
        if proj:
            proj_path = Path(proj)
            candidates = [
                proj_path / "Text",
                proj_path if proj_path.name.lower() == "text" else None,
                proj_path / "Translation" / "en" / "Text",
                proj_path / "UserData" / "Text",
            ]
            for cand in candidates:
                if cand and cand.is_dir():
                    p = cand
                    break
        if not p and getattr(self, "xuat_search_roots", None):
            for r in self.xuat_search_roots:
                if r.is_dir():
                    if r.name.lower() == "text":
                        p = r
                        break
                    if (r / "Text").is_dir():
                        p = r / "Text"
                        break
        if p and p.exists():
            subprocess.Popen(["explorer.exe", str(p)])
        else:
            messagebox.showinfo("Text Translation Folder", "Text translation folder could not be found. Configure the Project / Mod Folder in 'Configure Paths & Backups...'.")

    def on_open_redirected_resources_folder(self) -> None:
        """Open the RedirectedResources directory in Windows Explorer (supports BepInEx, MelonLoader, custom)."""
        p: Optional[Path] = None
        proj = getattr(self, "project_folder", None) or getattr(self, "bepinex_project_folder", None)
        if proj:
            proj_path = Path(proj)
            candidates = [
                proj_path / "RedirectedResources",
                proj_path.parent / "RedirectedResources",
                proj_path / "Translation" / "en" / "RedirectedResources",
                proj_path / "UserData" / "RedirectedResources",
                proj_path / "Mods" / "RedirectedResources",
            ]
            for cand in candidates:
                if cand.is_dir():
                    p = cand
                    break
        if p and p.exists():
            subprocess.Popen(["explorer.exe", str(p)])
        else:
            messagebox.showinfo("Redirected Resources Folder", "RedirectedResources folder could not be found. Configure the Project / Mod Folder in 'Configure Paths & Backups...'.")

    def on_open_selected_search_folder(self) -> None:
        """Open the currently selected search folder in Windows Explorer."""
        if getattr(self, "selected_search_folder", None) and Path(self.selected_search_folder).is_dir():
            subprocess.Popen(["explorer.exe", str(self.selected_search_folder)])
        else:
            messagebox.showinfo("Search Folder", "No search folder is currently set. Choose one using the [...] button in the search bar or drag & drop a folder.")

