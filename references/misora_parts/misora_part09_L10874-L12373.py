# ======================================================================
# FILE: misora.py — PART 09 / 10
# ORIGINAL LINE RANGE : L10874 .. L12373 (total 1500 lines of 12835)
# SOURCE SHA-256      : d23baae2be82fe93a18da7d3769af30d19ebe02a8b5f6a3645d56a6f53c0710e
# NOTE FOR AI REVIEWER: Cite ORIGINAL line numbers (L10874..L12373) and symbol names.
# SYMBOLS IN THIS PART (with exact original line numbers):
#   L10874:   MisoraApp.on_open_paths_dialog (def)
#   L11081:   MisoraApp._toggle_side_drawer_pin (def)
#   L11091:   MisoraApp.on_open_mtl_settings (def)
#   L11095:   MisoraApp.on_open_ai_prompt_settings (def)
#   L11099:   MisoraApp.on_open_translator_assistant (def)
#   L11108:   MisoraApp.on_translate_current_box (def)
#   L11170:   MisoraApp.on_batch_translate (def)
#   L11177:   MisoraApp.on_copy_ai_prompt (def)
#   L11209:   MisoraApp._show_paste_preview_and_apply (def)
#   L11396:   MisoraApp.on_paste_cross_box (def)
#   L11409:   MisoraApp.on_import_script (def)
#   L11451:   MisoraApp.on_export_script (def)
#   L11495:   MisoraApp.on_clear_dialogue_skeleton (def)
#   L11556:   MisoraApp.on_register_unity3d_association (def)
#   L11621:   MisoraApp.on_about (def)
#   L11636: class ScriptPastePreviewDialog
#   L11639:   ScriptPastePreviewDialog.__init__ (def)
#   L11696:   ScriptPastePreviewDialog._build_ui (def)
#   L11832:   ScriptPastePreviewDialog._populate_tree (def)
#   L11873:   ScriptPastePreviewDialog.on_apply (def)
#   L11880:   ScriptPastePreviewDialog.on_cancel (def)
#   L11889: class MTLSettingsDialog
#   L11891:   MTLSettingsDialog.__init__ (def)
#   L12045:   MTLSettingsDialog._on_cancel (def)
#   L12049:   MTLSettingsDialog._open_ai_prompt (def)
#   L12052:   MTLSettingsDialog._get_draft_config (def)
#   L12073:   MTLSettingsDialog._on_test_connection (def)
#   L12091:   MTLSettingsDialog._on_save (def)
#   L12104: class AIPromptSettingsDialog
#   L12106:   AIPromptSettingsDialog.__init__ (def)
#   L12206:   AIPromptSettingsDialog._on_cancel (def)
#   L12210:   AIPromptSettingsDialog._reset_default (def)
#   L12214:   AIPromptSettingsDialog._copy_prompt_now (def)
#   L12218:   AIPromptSettingsDialog._apply_settings_to_app (def)
#   L12224:   AIPromptSettingsDialog._save_and_close (def)
#   L12236: class TranslatorAssistantDialog
#   L12241:   TranslatorAssistantDialog.__init__ (def)
#   L12367:   TranslatorAssistantDialog._toggle_pin_top (def)
# ======================================================================

    def on_open_paths_dialog(self) -> None:
        """Dialog to configure Backup Folder, Project/Mod Folder, Datamine Tool, External Editors, Config, and Debug Log."""
        t = self.theme
        dlg = tk.Toplevel(self)
        dlg.title("Configure Paths, Backups & Folders")
        dlg.geometry("660x540")
        dlg.minsize(600, 480)
        dlg.transient(self)
        dlg.grab_set()
        dlg.configure(bg=t["bg_panel"])

        fg_panel = best_contrast_fg(t["bg_panel"])
        fg_editor = best_contrast_fg(t["bg_editor"])

        # 1. Pack bottom button bar FIRST so it stays anchored and visible
        btn_bar = tk.Frame(dlg, bg=t["bg_panel"], padx=16, pady=12)
        btn_bar.pack(side="bottom", fill="x")

        # 2. Main content frame
        content = tk.Frame(dlg, bg=t["bg_panel"], padx=16, pady=12)
        content.pack(side="top", fill="both", expand=True)

        def make_row(parent, label_text: str, browse_cmd=None, open_cmd=None, browse_text="Browse..."):
            r = tk.Frame(parent, bg=t["bg_panel"])
            r.pack(fill="x", pady=4)
            lbl = tk.Label(r, text=label_text, font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"], width=24, anchor="w")
            lbl.pack(side="left")
            if browse_cmd:
                btn_b = ttk.Button(r, text=browse_text, style="Small.TButton", command=browse_cmd)
                btn_b.pack(side="right", padx=(4, 0))
            if open_cmd:
                btn_o = ttk.Button(r, text="Open", style="Small.TButton", command=open_cmd)
                btn_o.pack(side="right", padx=(4, 0))
            ent = tk.Entry(r, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid")
            ent.pack(side="left", fill="x", expand=True, padx=4)
            return r, ent

        # 1. Backup Folder
        def _browse_bak():
            d = filedialog.askdirectory(title="Select Backup Folder")
            if d:
                ent_backup.delete(0, tk.END)
                ent_backup.insert(0, d)
                var_use_default_bak.set(False)

        def _open_bak_folder():
            b = ent_backup.get().strip() or str(SCRIPT_DIR / "backups")
            p = Path(b)
            p.mkdir(parents=True, exist_ok=True)
            subprocess.Popen(["explorer.exe", str(p)])

        r1, ent_backup = make_row(content, "Backup Folder:", browse_cmd=_browse_bak, open_cmd=_open_bak_folder)
        cur_bak = str(self.backup_folder) if self.backup_folder else str(SCRIPT_DIR / "backups")
        ent_backup.insert(0, cur_bak)
        var_use_default_bak = tk.BooleanVar(master=dlg, value=(self.backup_folder is None))

        cb_bak = tk.Checkbutton(
            content,
            text="Use default backups folder (SCRIPT_DIR/backups)",
            variable=var_use_default_bak,
            bg=t["bg_panel"],
            fg=fg_panel,
            selectcolor=t["bg_dark"],
            activebackground=t["bg_panel"],
            activeforeground=fg_panel,
        )
        cb_bak.pack(anchor="w", padx=(170, 0), pady=(0, 6))

        # 2. Project / Mod Root Folder (BepInEx, MelonLoader, XUAT, custom)
        def _browse_project():
            init_d = ent_project.get().strip() or self._get_project_display_path()
            d = filedialog.askdirectory(initialdir=init_d, title="Select Project Root / Mod Folder (BepInEx, MelonLoader, etc.)")
            if d:
                ent_project.delete(0, tk.END)
                ent_project.insert(0, d)

        def _open_project_folder_ui():
            b = ent_project.get().strip() or self._get_project_display_path()
            if b and Path(b).exists():
                subprocess.Popen(["explorer.exe", str(b)])
            else:
                messagebox.showinfo("Project Folder", "Folder does not exist.")

        r2, ent_project = make_row(content, "Project / Mod Folder:", browse_cmd=_browse_project, open_cmd=_open_project_folder_ui)
        cur_proj = str(self.project_folder) if getattr(self, "project_folder", None) else self._get_project_display_path()
        ent_project.insert(0, cur_proj)

        lbl_proj_hint = tk.Label(
            content,
            text="Root directory for translation/mod project (BepInEx, MelonLoader, XUAT, etc.)",
            font=("Segoe UI", 8),
            bg=t["bg_panel"],
            fg=t["fg_muted"]
        )
        lbl_proj_hint.pack(anchor="w", padx=(170, 0), pady=(0, 6))

        # 3. Universal Datamine Tool
        def _browse_datamine():
            f = filedialog.askopenfilename(
                title="Select Datamine Tool",
                filetypes=[("Executables & Scripts", "*.exe;*.py;*.bat;*.cmd"), ("All Files", "*.*")]
            )
            if f:
                ent_datamine.delete(0, tk.END)
                ent_datamine.insert(0, f)

        r3, ent_datamine = make_row(content, "Datamine Tool:", browse_cmd=_browse_datamine)
        if self.datamine_exe:
            ent_datamine.insert(0, str(self.datamine_exe))

        # 4. Notepad++ Path
        def _browse_npp():
            f = filedialog.askopenfilename(
                title="Select Notepad++ Executable",
                filetypes=[("Executables", "*.exe"), ("All Files", "*.*")]
            )
            if f:
                ent_npp.delete(0, tk.END)
                ent_npp.insert(0, f)

        r4, ent_npp = make_row(content, "Notepad++ Executable:", browse_cmd=_browse_npp)
        if self.notepadpp_path:
            ent_npp.insert(0, str(self.notepadpp_path))

        # 5. External Text Editor
        def _browse_editor():
            f = filedialog.askopenfilename(
                title="Select External Text Editor",
                filetypes=[("Executables & Scripts", "*.exe;*.bat;*.cmd"), ("All Files", "*.*")]
            )
            if f:
                ent_editor.delete(0, tk.END)
                ent_editor.insert(0, f)

        r5, ent_editor = make_row(content, "External Text Editor:", browse_cmd=_browse_editor)
        if self.external_editor_path:
            ent_editor.insert(0, str(self.external_editor_path))

        # Separator & File references
        ttk.Separator(content, orient="horizontal").pack(fill="x", pady=10)

        # 6. Config File
        r_cfg = tk.Frame(content, bg=t["bg_panel"])
        r_cfg.pack(fill="x", pady=2)
        tk.Label(r_cfg, text="Config File:", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["fg_muted"], width=24, anchor="w").pack(side="left")
        ttk.Button(r_cfg, text="Reveal", style="Small.TButton", command=lambda: subprocess.Popen(["explorer.exe", f"/select,{CONFIG_PATH}"])).pack(side="right", padx=(4, 0))
        tk.Label(r_cfg, text=str(CONFIG_PATH), font=("Consolas", 8), bg=t["bg_panel"], fg=fg_panel, anchor="w").pack(side="left", fill="x", expand=True)

        # 7. Debug Log
        r_log = tk.Frame(content, bg=t["bg_panel"])
        r_log.pack(fill="x", pady=2)
        tk.Label(r_log, text="Debug Log:", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["fg_muted"], width=24, anchor="w").pack(side="left")
        ttk.Button(r_log, text="Open", style="Small.TButton", command=self._on_open_debug_log_file).pack(side="right", padx=(4, 0))
        tk.Label(r_log, text=str(DEBUG_LOG_PATH), font=("Consolas", 8), bg=t["bg_panel"], fg=fg_panel, anchor="w").pack(side="left", fill="x", expand=True)

        # Buttons at bottom
        def _safe_close(_e: Optional[tk.Event] = None) -> None:
            safe_grab_release(dlg)
            if dlg.winfo_exists():
                dlg.destroy()

        def _save_and_close():
            if var_use_default_bak.get():
                self.backup_folder = None
            else:
                b_val = ent_backup.get().strip()
                self.backup_folder = Path(b_val) if b_val else None

            proj_val = ent_project.get().strip()
            if proj_val:
                p = Path(proj_val)
                self._set_project_folder(p)
                if self.scope_var.get() == "project":
                    self.folder_path_var.set(str(self.project_folder))
            else:
                self.project_folder = None
                self.bepinex_project_folder = None
                self.xuat_search_roots = []

            dm_val = ent_datamine.get().strip()
            self.datamine_exe = Path(dm_val) if dm_val else None

            npp_val = ent_npp.get().strip()
            self.notepadpp_path = Path(npp_val) if npp_val else None

            ed_val = ent_editor.get().strip()
            self.external_editor_path = Path(ed_val) if ed_val else None

            self._save_user_prefs()
            self.lbl_status.config(text="Updated paths and backup configuration.")
            self.show_toast("Paths and backup settings saved successfully!")
            _safe_close()
            messagebox.showinfo(
                "Settings Saved",
                "Paths, backups, and preferences have been saved successfully.",
                parent=self,
            )

        dlg.protocol("WM_DELETE_WINDOW", _safe_close)
        dlg.bind("<Escape>", _safe_close)

        ttk.Button(btn_bar, text="Cancel", style="TButton", command=_safe_close).pack(side="right", padx=4)
        ttk.Button(btn_bar, text="Save & Apply", style="Pink.TButton", command=_save_and_close).pack(side="right", padx=4)

    # -------------------------------------------------------------------------
    # Side Drawer Pinning (#6)
    # -------------------------------------------------------------------------
    def _toggle_side_drawer_pin(self) -> None:
        self._side_drawer_pinned = not getattr(self, "_side_drawer_pinned", False)
        pin_icon = "📌" if self._side_drawer_pinned else "📍"
        if hasattr(self, "btn_drawer_pin"):
            self.btn_drawer_pin.config(text=pin_icon)
        self.show_toast(f"Side drawer {'pinned' if self._side_drawer_pinned else 'unpinned'}")

    # -------------------------------------------------------------------------
    # Translator Suite Callbacks & Handlers (#4A, #16, #17)
    # -------------------------------------------------------------------------
    def on_open_mtl_settings(self) -> None:
        """Open the Machine Translation sources & configuration dialog."""
        MTLSettingsDialog(self)

    def on_open_ai_prompt_settings(self) -> None:
        """Open the AI / LLM translation prompt header and exporter dialog."""
        AIPromptSettingsDialog(self)

    def on_open_translator_assistant(self) -> None:
        """Open or focus the floating Translator Assistant workspace window."""
        if hasattr(self, "_translator_dialog") and self._translator_dialog and self._translator_dialog.winfo_exists():
            self._translator_dialog.lift()
            self._translator_dialog.focus_force()
            self._translator_dialog.refresh_box()
            return
        self._translator_dialog = TranslatorAssistantDialog(self)

    def on_translate_current_box(self) -> None:
        """Translate the dialogue in the active box using configured active engine (F8)."""
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

        def on_success(result: str):
            def update_ui():
                if not self.current_doc or b_idx >= len(self.current_doc.boxes):
                    return
                old_b = self.current_doc.boxes[b_idx]
                self.undo_journal.record(
                    BoxEditDelta(
                        box_index=b_idx,
                        old_speaker=old_b.speaker,
                        new_speaker=old_b.speaker,
                        old_text=old_b.clean_text,
                        new_text=result,
                        file_path=str(self.current_file_path) if self.current_file_path else "",
                        box_uid=old_b.uid,
                        source="mtl",
                    )
                )
                self.current_doc.inject_box(b_idx, old_b.speaker, result)
                self._modified_boxes.add(b_idx)
                self._mark_document_dirty(self.current_file_path)
                self._dirty_state_changed()
                self._update_views()
                self.show_toast(f"✓ Translated Box {b_idx + 1} via {engine_name}")
                self.lbl_status.config(text=f"Box {b_idx + 1} translated via {engine_name}")
            self.after_idle(update_ui)

        def on_error(err: str):
            def show_err():
                self.logger.error("MTL", f"Translation failed for Box {b_idx + 1}: {err}")
                self.show_toast(f"❌ Translation failed: {err}")
                self.lbl_status.config(text=f"Translation failed: {err}")
            self.after_idle(show_err)

        translate_async(
            orig_text,
            self.mtl_config,
            on_success=on_success,
            on_error=on_error,
            xuat_cache=getattr(self, "xuat_entries", None),
        )

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
# Translator Suite Dialogs (#4A, #16, #17)
# =============================================================================
class MTLSettingsDialog(tk.Toplevel):
    """Configuration dialog for Machine Translation providers, API keys, endpoints and options."""
    def __init__(self, parent: "MisoraApp"):
        super().__init__(parent)
        self.app = parent
        self.title("Configure MTL Sources & Keys")
        self.geometry("640x600")
        self.minsize(580, 520)
        self.transient(parent)
        self.grab_set()

        t = self.app.theme
        self.configure(bg=t["bg_panel"])
        apply_window_icon(self)

        fg_panel = best_contrast_fg(t["bg_panel"])
        fg_editor = best_contrast_fg(t["bg_editor"])

        content = tk.Frame(self, bg=t["bg_panel"], padx=18, pady=12)
        content.pack(fill="both", expand=True)

        hdr = tk.Frame(content, bg=t["bg_panel"])
        hdr.pack(fill="x", pady=(0, 10))
        tk.Label(
            hdr,
            text="Machine Translation & External Providers",
            font=("Segoe UI", 12, "bold"),
            bg=t["bg_panel"],
            fg=t["misora_pink"],
        ).pack(side="left")

        # Active Engine Row
        r_eng = tk.Frame(content, bg=t["bg_panel"])
        r_eng.pack(fill="x", pady=4)
        tk.Label(r_eng, text="Active Engine:", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=fg_panel, width=18, anchor="w").pack(side="left")
        self.var_engine = tk.StringVar(master=self, value=self.app.mtl_config.active_engine)
        cb_engine = ttk.Combobox(r_eng, textvariable=self.var_engine, values=MTL_ENGINES, state="readonly", width=22)
        cb_engine.pack(side="left", padx=4)

        # Languages Row
        r_lang = tk.Frame(content, bg=t["bg_panel"])
        r_lang.pack(fill="x", pady=4)
        tk.Label(r_lang, text="Languages:", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=fg_panel, width=18, anchor="w").pack(side="left")
        tk.Label(r_lang, text="From:", bg=t["bg_panel"], fg=t["fg_muted"]).pack(side="left")
        self.var_src = tk.StringVar(master=self, value=self.app.mtl_config.src_lang)
        ent_src = tk.Entry(r_lang, textvariable=self.var_src, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid", width=6)
        ent_src.pack(side="left", padx=(2, 10))
        tk.Label(r_lang, text="To:", bg=t["bg_panel"], fg=t["fg_muted"]).pack(side="left")
        self.var_tgt = tk.StringVar(master=self, value=self.app.mtl_config.tgt_lang)
        ent_tgt = tk.Entry(r_lang, textvariable=self.var_tgt, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid", width=6)
        ent_tgt.pack(side="left", padx=2)
        tk.Label(r_lang, text="(e.g. ja -> en)", font=("Segoe UI", 8), bg=t["bg_panel"], fg=t["fg_muted"]).pack(side="left", padx=8)

        ttk.Separator(content, orient="horizontal").pack(fill="x", pady=8)

        # DeepL Section
        sec_deepl = tk.LabelFrame(content, text="DeepL API Settings", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"], padx=10, pady=8)
        sec_deepl.pack(fill="x", pady=4)

        r_dp1 = tk.Frame(sec_deepl, bg=t["bg_panel"])
        r_dp1.pack(fill="x", pady=2)
        tk.Label(r_dp1, text="Auth Key:", font=("Segoe UI", 9), bg=t["bg_panel"], fg=fg_panel, width=16, anchor="w").pack(side="left")
        self.var_deepl_key = tk.StringVar(master=self, value=self.app.mtl_config.deepl_api_key)
        self.ent_deepl_key = tk.Entry(r_dp1, textvariable=self.var_deepl_key, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid", show="*")
        self.ent_deepl_key.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.var_show_key = tk.BooleanVar(master=self, value=False)
        def _toggle_key():
            self.ent_deepl_key.config(show="" if self.var_show_key.get() else "*")
        tk.Checkbutton(r_dp1, text="Show", variable=self.var_show_key, command=_toggle_key, bg=t["bg_panel"], fg=fg_panel, selectcolor=t["bg_dark"]).pack(side="left")

        r_dp2 = tk.Frame(sec_deepl, bg=t["bg_panel"])
        r_dp2.pack(fill="x", pady=2)
        self.var_deepl_pro = tk.BooleanVar(master=self, value=self.app.mtl_config.deepl_use_pro)
        tk.Checkbutton(
            r_dp2,
            text="Use DeepL Pro subscription endpoint (api.deepl.com instead of api-free.deepl.com)",
            variable=self.var_deepl_pro,
            bg=t["bg_panel"],
            fg=fg_panel,
            selectcolor=t["bg_dark"],
        ).pack(side="left")

        # Local MT Section
        sec_local = tk.LabelFrame(content, text="Local MT / Sugoi / LibreTranslate", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"], padx=10, pady=8)
        sec_local.pack(fill="x", pady=4)

        r_loc = tk.Frame(sec_local, bg=t["bg_panel"])
        r_loc.pack(fill="x", pady=2)
        tk.Label(r_loc, text="Server URL:", font=("Segoe UI", 9), bg=t["bg_panel"], fg=fg_panel, width=16, anchor="w").pack(side="left")
        self.var_local_url = tk.StringVar(master=self, value=self.app.mtl_config.local_mtl_url)
        ent_loc = tk.Entry(r_loc, textvariable=self.var_local_url, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid")
        ent_loc.pack(side="left", fill="x", expand=True)
        tk.Label(sec_local, text="Default Sugoi Toolkit: http://127.0.0.1:14366  |  LibreTranslate: http://127.0.0.1:5000/translate", font=("Segoe UI", 8), bg=t["bg_panel"], fg=t["fg_muted"]).pack(anchor="w", pady=(2, 0))

        # LLM Section
        sec_llm = tk.LabelFrame(content, text="OpenAI / LLM Endpoint (Ollama, LM Studio, etc.)", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"], padx=10, pady=8)
        sec_llm.pack(fill="x", pady=4)

        r_llm1 = tk.Frame(sec_llm, bg=t["bg_panel"])
        r_llm1.pack(fill="x", pady=2)
        tk.Label(r_llm1, text="Base URL:", font=("Segoe UI", 9), bg=t["bg_panel"], fg=fg_panel, width=16, anchor="w").pack(side="left")
        self.var_llm_url = tk.StringVar(master=self, value=self.app.mtl_config.llm_base_url)
        ent_llm_url = tk.Entry(r_llm1, textvariable=self.var_llm_url, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid")
        ent_llm_url.pack(side="left", fill="x", expand=True)

        r_llm2 = tk.Frame(sec_llm, bg=t["bg_panel"])
        r_llm2.pack(fill="x", pady=2)
        tk.Label(r_llm2, text="Model Name:", font=("Segoe UI", 9), bg=t["bg_panel"], fg=fg_panel, width=16, anchor="w").pack(side="left")
        self.var_llm_model = tk.StringVar(master=self, value=self.app.mtl_config.llm_model)
        ent_llm_model = tk.Entry(r_llm2, textvariable=self.var_llm_model, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid", width=24)
        ent_llm_model.pack(side="left", padx=(0, 10))

        tk.Label(r_llm2, text="API Key (optional):", font=("Segoe UI", 9), bg=t["bg_panel"], fg=fg_panel).pack(side="left")
        self.var_llm_key = tk.StringVar(master=self, value=self.app.mtl_config.llm_api_key)
        ent_llm_key = tk.Entry(r_llm2, textvariable=self.var_llm_key, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid", show="*")
        ent_llm_key.pack(side="left", fill="x", expand=True, padx=(4, 0))

        # Behavior & Cache Section
        sec_opt = tk.Frame(content, bg=t["bg_panel"])
        sec_opt.pack(fill="x", pady=6)

        self.var_protect = tk.BooleanVar(master=self, value=self.app.mtl_config.protect_tags)
        tk.Checkbutton(sec_opt, text="Shield NGUI tags, Ruby tags & {playername} during translation", variable=self.var_protect, bg=t["bg_panel"], fg=fg_panel, selectcolor=t["bg_dark"]).pack(anchor="w")

        self.var_xuat_cache = tk.BooleanVar(master=self, value=self.app.mtl_config.use_xuat_cache)
        tk.Checkbutton(sec_opt, text="Use loaded XUAT translation dictionary as instant offline lookup", variable=self.var_xuat_cache, bg=t["bg_panel"], fg=fg_panel, selectcolor=t["bg_dark"]).pack(anchor="w")

        r_to = tk.Frame(sec_opt, bg=t["bg_panel"])
        r_to.pack(fill="x", pady=2)
        tk.Label(r_to, text="Timeout (sec):", bg=t["bg_panel"], fg=fg_panel).pack(side="left")
        self.var_timeout = tk.DoubleVar(master=self, value=self.app.mtl_config.timeout_sec)
        sp_to = ttk.Spinbox(r_to, from_=3.0, to=60.0, increment=1.0, textvariable=self.var_timeout, width=6)
        sp_to.pack(side="left", padx=6)

        # Connection Test Box
        tst_box = tk.Frame(content, bg=t["bg_editor"], bd=1, relief="solid", padx=8, pady=6)
        tst_box.pack(fill="x", pady=6)

        self.lbl_tst_result = tk.Label(tst_box, text="Click 'Test Connection' to verify active engine.", font=("Segoe UI", 9), bg=t["bg_editor"], fg=t["fg_muted"], anchor="w")
        self.lbl_tst_result.pack(side="left", fill="x", expand=True)

        self.btn_tst = ttk.Button(tst_box, text="Test Connection", style="Small.TButton", command=self._on_test_connection)
        self.btn_tst.pack(side="right")

        # Bottom Buttons
        btn_bar = tk.Frame(self, bg=t["bg_panel"], padx=18, pady=12)
        btn_bar.pack(fill="x", side="bottom")

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.bind("<Escape>", lambda _e=None: self._on_cancel())

        ttk.Button(btn_bar, text="Cancel", style="TButton", command=self._on_cancel).pack(side="right", padx=4)
        ttk.Button(btn_bar, text="Save & Apply", style="Pink.TButton", command=self._on_save).pack(side="right", padx=4)

        ttk.Button(btn_bar, text="AI Prompt Settings...", style="Small.TButton", command=self._open_ai_prompt).pack(side="left")

    def _on_cancel(self) -> None:
        safe_grab_release(self)
        self.destroy()

    def _open_ai_prompt(self):
        self.app.on_open_ai_prompt_settings()

    def _get_draft_config(self) -> MTLConfig:
        cfg = MTLConfig(
            active_engine=self.var_engine.get(),
            src_lang=self.var_src.get().strip() or "ja",
            tgt_lang=self.var_tgt.get().strip() or "en",
            deepl_api_key=self.var_deepl_key.get().strip(),
            deepl_use_pro=self.var_deepl_pro.get(),
            local_mtl_url=self.var_local_url.get().strip(),
            llm_base_url=self.var_llm_url.get().strip(),
            llm_api_key=self.var_llm_key.get().strip(),
            llm_model=self.var_llm_model.get().strip() or "qwen2.5:7b",
            llm_system_prompt=self.app.mtl_config.llm_system_prompt,
            protect_tags=self.var_protect.get(),
            use_xuat_cache=self.var_xuat_cache.get(),
            timeout_sec=float(self.var_timeout.get()),
            rate_limit_delay=self.app.mtl_config.rate_limit_delay,
            ai_prompt_include_header=self.app.mtl_config.ai_prompt_include_header,
            ai_prompt_include_speaker=self.app.mtl_config.ai_prompt_include_speaker,
        )
        return cfg

    def _on_test_connection(self):
        cfg = self._get_draft_config()
        self.lbl_tst_result.config(text=f"Testing {cfg.active_engine}...", fg=self.app.theme["fg_text"])
        self.btn_tst.config(state="disabled")

        def worker():
            engine = MTLEngine(cfg)
            ok, msg = engine.test_connection(cfg)
            def update():
                if self.winfo_exists():
                    self.btn_tst.config(state="normal")
                    col = self.app.theme.get("accent_green", "#2e7d32") if ok else self.app.theme.get("accent_yellow", "#f57c00")
                    self.lbl_tst_result.config(text=msg, fg=col)
            self.after_idle(update)

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _on_save(self):
        self.app.mtl_config = self._get_draft_config()
        self.app._save_user_prefs()
        self.app.show_toast(f"✓ Saved MTL preferences ({self.app.mtl_config.active_engine})")
        safe_grab_release(self)
        self.destroy()
        messagebox.showinfo(
            "Settings Saved",
            f"Machine Translation settings ({self.app.mtl_config.active_engine}) have been saved.",
            parent=self.app,
        )


class AIPromptSettingsDialog(tk.Toplevel):
    """Configuration dialog for AI Prompt Header, Instructions, and Script Exporter."""
    def __init__(self, parent: "MisoraApp"):
        super().__init__(parent)
        self.app = parent
        self.title("AI / LLM Prompt & Script Settings")
        self.geometry("680x560")
        self.minsize(580, 480)
        self.transient(parent)
        self.grab_set()

        t = self.app.theme
        self.configure(bg=t["bg_panel"])
        apply_window_icon(self)

        fg_panel = best_contrast_fg(t["bg_panel"])
        fg_editor = best_contrast_fg(t["bg_editor"])

        content = tk.Frame(self, bg=t["bg_panel"], padx=18, pady=12)
        content.pack(fill="both", expand=True)

        tk.Label(
            content,
            text="AI Translation Prompt Header & Rules",
            font=("Segoe UI", 12, "bold"),
            bg=t["bg_panel"],
            fg=t["misora_pink"],
        ).pack(anchor="w", pady=(0, 6))

        tk.Label(
            content,
            text=(
                "Customize the system rules and context given to AI translation models (ChatGPT, Claude, Ollama, etc.).\n"
                "The header will be prepended when you copy the entire script using 'Copy AI Translation Prompt'."
            ),
            font=("Segoe UI", 9),
            bg=t["bg_panel"],
            fg=t["fg_muted"],
            justify="left",
        ).pack(anchor="w", pady=(0, 8))

        # Checkboxes
        opts_frame = tk.Frame(content, bg=t["bg_panel"])
        opts_frame.pack(fill="x", pady=4)

        self.var_include_hdr = tk.BooleanVar(master=self, value=self.app.mtl_config.ai_prompt_include_header)
        tk.Checkbutton(
            opts_frame,
            text="Include Prompt Header & Rules when copying script",
            variable=self.var_include_hdr,
            bg=t["bg_panel"],
            fg=fg_panel,
            selectcolor=t["bg_dark"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        self.var_include_spk = tk.BooleanVar(master=self, value=self.app.mtl_config.ai_prompt_include_speaker)
        tk.Checkbutton(
            opts_frame,
            text="Include Speaker Names in Box delimiters (=== [BOX:0|Speaker:コッコロ] ===)",
            variable=self.var_include_spk,
            bg=t["bg_panel"],
            fg=fg_panel,
            selectcolor=t["bg_dark"],
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        # Multi-line text for header
        txt_frame = tk.Frame(content, bg=t["bg_editor"], bd=1, relief="solid")
        txt_frame.pack(fill="both", expand=True, pady=8)

        self.txt_prompt = tk.Text(
            txt_frame,
            wrap="word",
            font=("Segoe UI", 9),
            bg=t["bg_editor"],
            fg=fg_editor,
            insertbackground=t["misora_pink"],
            bd=0,
            padx=8,
            pady=8,
        )
        sb = tk.Scrollbar(txt_frame, command=self.txt_prompt.yview)
        sb.pack(side="right", fill="y")
        self.txt_prompt.pack(side="left", fill="both", expand=True)
        self.txt_prompt.config(yscrollcommand=sb.set)

        self.txt_prompt.insert("1.0", self.app.mtl_config.llm_system_prompt)

        # Bottom buttons
        btn_bar = tk.Frame(self, bg=t["bg_panel"], padx=18, pady=12)
        btn_bar.pack(fill="x", side="bottom")

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.bind("<Escape>", lambda _e=None: self._on_cancel())

        ttk.Button(btn_bar, text="Reset to Recommended Default", style="Small.TButton", command=self._reset_default).pack(side="left")
        ttk.Button(btn_bar, text="📋 Copy Script with Prompt Now", style="Small.TButton", command=self._copy_prompt_now).pack(side="left", padx=8)

        ttk.Button(btn_bar, text="Cancel", style="TButton", command=self._on_cancel).pack(side="right", padx=4)
        ttk.Button(btn_bar, text="Save & Close", style="Pink.TButton", command=self._save_and_close).pack(side="right", padx=4)

    def _on_cancel(self) -> None:
        safe_grab_release(self)
        self.destroy()

    def _reset_default(self):
        self.txt_prompt.delete("1.0", tk.END)
        self.txt_prompt.insert("1.0", DEFAULT_LLM_PROMPT)

    def _copy_prompt_now(self):
        self._apply_settings_to_app()
        self.app.on_copy_ai_prompt()

    def _apply_settings_to_app(self):
        self.app.mtl_config.llm_system_prompt = self.txt_prompt.get("1.0", tk.END).strip()
        self.app.mtl_config.ai_prompt_include_header = self.var_include_hdr.get()
        self.app.mtl_config.ai_prompt_include_speaker = self.var_include_spk.get()
        self.app._save_user_prefs(silent=True)

    def _save_and_close(self):
        self._apply_settings_to_app()
        self.app.show_toast("✓ Saved AI prompt configuration")
        safe_grab_release(self)
        self.destroy()
        messagebox.showinfo(
            "Settings Saved",
            "AI translation prompt header & settings have been saved.",
            parent=self.app,
        )


class TranslatorAssistantDialog(tk.Toplevel):
    """
    Dedicated floating Translation Assistant workspace.
    Displays original Japanese, active engine output, comparison cards, and 1-click apply.
    """
    def __init__(self, parent: "MisoraApp"):
        super().__init__(parent)
        self.app = parent
        self.title("Misora - Translator Assistant")
        self.geometry("620x580")
        self.minsize(540, 480)
        self.transient(parent)

        t = self.app.theme
        self.configure(bg=t["bg_panel"])
        apply_window_icon(self)

        fg_panel = best_contrast_fg(t["bg_panel"])
        fg_editor = best_contrast_fg(t["bg_editor"])

        # Top Bar: Box navigation and engine selector
        top_bar = tk.Frame(self, bg=t["bg_panel"], padx=14, pady=8)
        top_bar.pack(fill="x")

        self.lbl_box_info = tk.Label(
            top_bar,
            text="Box 0 / 0",
            font=("Segoe UI", 10, "bold"),
            bg=t["bg_panel"],
            fg=t["misora_pink"],
        )
        self.lbl_box_info.pack(side="left")

        ttk.Button(top_bar, text="< Prev", style="Nav.TButton", command=self._on_prev).pack(side="left", padx=(10, 2))
        ttk.Button(top_bar, text="Next >", style="Nav.TButton", command=self._on_next).pack(side="left", padx=2)

        self.lbl_speaker = tk.Label(
            top_bar,
            text="Speaker: -",
            font=("Segoe UI", 9),
            bg=t["bg_panel"],
            fg=t["fg_muted"],
        )
        self.lbl_speaker.pack(side="left", padx=(10, 0))

        # Pin on Top & Engine selector on right (#6)
        self._is_pinned_top = False
        self.btn_pin = ttk.Button(
            top_bar,
            text="📌",
            style="Small.TButton",
            width=3,
            command=self._toggle_pin_top,
        )
        self.btn_pin.pack(side="right", padx=(4, 0))

        # Engine selector on right
        self.var_engine = tk.StringVar(master=self, value=self.app.mtl_config.active_engine)
        cb = ttk.Combobox(top_bar, textvariable=self.var_engine, values=MTL_ENGINES, state="readonly", width=14)
        cb.pack(side="right", padx=(4, 0))
        cb.bind("<<ComboboxSelected>>", self._on_engine_change)

        ttk.Button(top_bar, text="Fetch All", style="Small.TButton", command=self._on_fetch_all).pack(side="right", padx=2)
        ttk.Button(top_bar, text="Translate (F8)", style="Pink.TButton", command=self._on_translate).pack(side="right", padx=2)

        # Original Japanese Box
        orig_frame = tk.LabelFrame(self, text="Original Dialogue (Japanese)", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=fg_panel, padx=10, pady=6)
        orig_frame.pack(fill="x", padx=14, pady=(4, 6))

        self.txt_orig = tk.Text(
            orig_frame,
            wrap="word",
            height=4,
            font=("Segoe UI", 10),
            bg=t["bg_editor"],
            fg=fg_editor,
            bd=1,
            relief="solid",
            padx=6,
            pady=6,
        )
        self.txt_orig.pack(fill="x")

        # Translated Dialogue Box
        trans_frame = tk.LabelFrame(self, text="Translated Dialogue (Editable)", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"], padx=10, pady=6)
        trans_frame.pack(fill="both", expand=True, padx=14, pady=4)

        self.txt_trans = tk.Text(
            trans_frame,
            wrap="word",
            font=("Segoe UI", 10),
            bg=t["bg_editor"],
            fg=fg_editor,
            insertbackground=t["misora_pink"],
            bd=1,
            relief="solid",
            padx=6,
            pady=6,
        )
        self.txt_trans.pack(fill="both", expand=True)

        # Multi-engine comparison frame (collapsible)
        self.comp_frame = tk.LabelFrame(self, text="Engine Comparison", font=("Segoe UI", 8, "bold"), bg=t["bg_panel"], fg=t["fg_muted"], padx=8, pady=4)

        # Status / Feedback label
        self.lbl_status = tk.Label(self, text="Ready", font=("Segoe UI", 8), bg=t["bg_panel"], fg=t["fg_muted"], anchor="w", padx=14)
        self.lbl_status.pack(fill="x", pady=(2, 0))

        # Bottom Action Bar
        btn_bar = tk.Frame(self, bg=t["bg_panel"], padx=14, pady=10)
        btn_bar.pack(fill="x", side="bottom")

        ttk.Button(btn_bar, text="Close", style="TButton", command=self._on_close).pack(side="right", padx=4)
        ttk.Button(btn_bar, text="Copy Translation", style="Small.TButton", command=self._on_copy).pack(side="right", padx=4)
        ttk.Button(btn_bar, text="Apply & Next (Alt+S)", style="TButton", command=self._on_apply_and_next).pack(side="right", padx=4)
        ttk.Button(btn_bar, text="Apply to Box (Ctrl+Enter)", style="Pink.TButton", command=self._on_apply).pack(side="right", padx=4)

        ttk.Button(btn_bar, text="Configure Engines...", style="Small.TButton", command=self.app.on_open_mtl_settings).pack(side="left")

        # Key bindings
        self.bind("<Escape>", lambda _e=None: self._on_close())
        self.bind("<F8>", lambda e: self._on_translate())
        self.bind("<Control-Return>", lambda e: self._on_apply())
        self.bind("<Alt-Left>", lambda e: self._on_prev())
        self.bind("<Alt-Right>", lambda e: self._on_next())
        self.bind("<Alt-s>", lambda e: self._on_apply_and_next())
        self.bind("<Alt-S>", lambda e: self._on_apply_and_next())

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.refresh_box()

    def _toggle_pin_top(self):
        self._is_pinned_top = not getattr(self, "_is_pinned_top", False)
        self.wm_attributes("-topmost", self._is_pinned_top)
        self.btn_pin.configure(text="📌" if self._is_pinned_top else "📍")
        status = "pinned on top" if self._is_pinned_top else "unpinned"
        self.app.show_toast(f"Translator Assistant {status}")

