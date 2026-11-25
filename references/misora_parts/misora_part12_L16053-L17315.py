# misora.py PART 12/12 | ORIG L16053-L17315/17315 | SHA:ec4d9bfc8ec6
# SYMS: L16053:ImportFromXUATDialog._on_apply_import, L16153:ImportFromXUATDialog._on_close, L16176:class MTLSettingsDialog, L16178:MTLSettingsDialog.__init__, L16338:MTLSettingsDialog._on_cancel, L16342:MTLSettingsDialog._open_ai_prompt, L16345:MTLSettingsDialog._get_draft_config, L16366:MTLSettingsDialog._on_test_connection, L16384:MTLSettingsDialog._schedule_poll, L16394:MTLSettingsDialog._poll_worker_queue, L16414:MTLSettingsDialog._on_close, L16425:MTLSettingsDialog._on_save, L16447:class AIPromptSettingsDialog, L16449:AIPromptSettingsDialog.__init__, L16549:AIPromptSettingsDialog._on_cancel, L16553:AIPromptSettingsDialog._reset_default, L16557:AIPromptSettingsDialog._copy_prompt_now, L16561:AIPromptSettingsDialog._apply_settings_to_app, L16567:AIPromptSettingsDialog._save_and_close, L16579:class TranslatorAssistantDialog, L16584:TranslatorAssistantDialog.__init__, L16715:TranslatorAssistantDialog._toggle_pin_top, L16722:TranslatorAssistantDialog._schedule_poll, L16732:TranslatorAssistantDialog._poll_worker_queue, L16803:TranslatorAssistantDialog._on_close, L16815:TranslatorAssistantDialog._on_engine_change, L16819:TranslatorAssistantDialog.refresh_box, L16847:TranslatorAssistantDialog._on_prev, L16851:TranslatorAssistantDialog._on_next, L16855:TranslatorAssistantDialog._on_translate, L16898:TranslatorAssistantDialog._on_fetch_all, L16962:TranslatorAssistantDialog._use_comp_text, L16966:TranslatorAssistantDialog._on_apply, L17009:TranslatorAssistantDialog._on_apply_and_next, L17013:TranslatorAssistantDialog._on_copy, L17021:class BatchTranslateDialog, L17023:BatchTranslateDialog.__init__, L17095:BatchTranslateDialog._end_undo_batch, L17104:BatchTranslateDialog._schedule_poll, L17114:BatchTranslateDialog._on_close, L17136:BatchTranslateDialog._start_batch, L17220:BatchTranslateDialog._poll_worker_queue, L17292:def main

    def _on_apply_import(self) -> bool:
        """Show Pre-Apply summary prompt and apply unlocked, non-skipped boxes in ONE Undo batch."""
        doc = self.app.current_doc
        if not doc or not doc.boxes:
            return False

        translate_speakers = bool(self.var_translate_speakers.get())
        to_import_nums: List[int] = []
        lock_skipped_nums: List[int] = []
        user_skipped_nums: List[int] = []
        missing_count = 0
        plan: List[Tuple[int, Any, str, str]] = []

        for row in self._rows:
            b_idx = row["box_idx"]
            b_num = b_idx + 1
            if self.app.is_box_locked(b_idx) or row["is_locked"]:
                lock_skipped_nums.append(b_num)
                continue
            if row["var_skip"].get():
                user_skipped_nums.append(b_num)
                continue
            cands = row["candidates"]
            if not cands:
                missing_count += 1
                continue
            box = doc.boxes[b_idx]
            new_tx = cands[row["cand_idx"]].value
            new_sp = box.speaker
            if translate_speakers and b_idx in self._speaker_matches and box.kind == "print":
                new_sp = self._speaker_matches[b_idx]
            to_import_nums.append(b_num)
            plan.append((b_idx, row["box_uid"], new_sp, new_tx))

        prompt = (
            "Confirm XUAT Import Summary:\n\n"
            f"1. Boxes to import ({len(to_import_nums)}): {self._format_box_list(to_import_nums)}\n"
            f"2. Skipped — Translation Lock (🔒) ({len(lock_skipped_nums)}): {self._format_box_list(lock_skipped_nums)}\n"
            f"3. Skipped — User Skip ({len(user_skipped_nums)}): {self._format_box_list(user_skipped_nums)}\n"
            f"4. Missing / Untranslated: {missing_count} box(es)\n\n"
            "Proceed with importing these translations?"
        )
        if not messagebox.askyesno("Confirm XUAT Import", prompt, parent=self):
            return False

        if not plan:
            self.app.show_toast("No eligible boxes to import.")
            return False

        self.app._commit_widget_edit()

        applied_count = 0
        self.app.undo_journal.begin_batch("Import from XUAT")
        try:
            for b_idx, b_uid, new_sp, new_tx in plan:
                if not (0 <= b_idx < len(doc.boxes)):
                    continue
                if self.app.is_box_locked(b_idx):
                    continue
                old_box = doc.boxes[b_idx]
                old_sp = old_box.speaker
                old_tx = old_box.clean_text
                if new_sp == old_sp and new_tx == old_tx:
                    continue
                old_segs = [s.text for s in old_box.segs]
                # Mutate AST first (BUG-13)
                doc.inject_box(b_idx, new_sp, new_tx)
                new_segs = [s.text for s in doc.boxes[b_idx].segs]
                self.app.undo_journal.record(
                    BoxEditDelta(
                        box_index=b_idx,
                        old_speaker=old_sp,
                        new_speaker=new_sp,
                        old_text=old_tx,
                        new_text=new_tx,
                        file_path=str(self.app.current_file_path) if self.app.current_file_path else "",
                        box_uid=b_uid,
                        source="xuat_import",
                        old_seg_texts=old_segs,
                        new_seg_texts=new_segs,
                    )
                )
                self.app._modified_boxes.add(b_idx)
                if b_uid is not None and hasattr(self.app, "_modified_box_uids"):
                    self.app._modified_box_uids.add(b_uid)
                applied_count += 1
        finally:
            self.app.undo_journal.end_batch()

        if applied_count > 0:
            self.app._mark_document_dirty(self.app.current_file_path)
            self.app._dirty_state_changed()
            self.app._update_views()
            self.app.show_toast(f"✓ Imported XUAT translations for {applied_count} box(es)")
        else:
            self.app.show_toast("No changes were applied from XUAT.")

        self._on_close()
        return applied_count > 0

    def _on_close(self) -> None:
        self._focused_box_widget = None
        self._rows.clear()
        self._filter_buttons.clear()
        self._speaker_matches.clear()
        self.var_translate_speakers = None
        try:
            for w in (self.list_canvas, self.rows_frame):
                if w and w.winfo_exists():
                    w.unbind("<MouseWheel>")
                    w.unbind("<Configure>")
        except Exception:
            pass
        if getattr(self.app, "_import_xuat_dialog", None) is self:
            self.app._import_xuat_dialog = None
        safe_grab_release(self)
        if self.winfo_exists():
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

        self.worker_queue: queue.Queue = queue.Queue()
        self._test_seq: int = 0
        self._poll_job: Optional[str] = None
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.bind("<Escape>", lambda _e=None: self._on_close())

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

        self._test_seq += 1
        seq = self._test_seq
        q = self.worker_queue

        def worker():
            engine = MTLEngine(cfg)
            ok, msg = engine.test_connection(cfg)
            q.put(("test_result", seq, ok, msg))

        t = threading.Thread(target=worker, daemon=True)
        t.start()
        self._schedule_poll()

    def _schedule_poll(self):
        if self._poll_job:
            try:
                self.after_cancel(self._poll_job)
            except Exception:
                pass
            self._poll_job = None
        if self.winfo_exists():
            self._poll_job = self.after(50, self._poll_worker_queue)

    def _poll_worker_queue(self):
        self._poll_job = None
        if not self.winfo_exists():
            return

        try:
            while True:
                msg = self.worker_queue.get_nowait()
                if msg[0] == "test_result":
                    _, seq, ok, text = msg
                    if seq == self._test_seq and self.winfo_exists():
                        self.btn_tst.config(state="normal")
                        col = self.app.theme.get("accent_green", "#2e7d32") if ok else self.app.theme.get("accent_yellow", "#f57c00")
                        self.lbl_tst_result.config(text=text, fg=col)
        except queue.Empty:
            pass

        if self.winfo_exists() and str(self.btn_tst.cget("state")) == "disabled":
            self._schedule_poll()

    def _on_close(self):
        if self._poll_job:
            try:
                self.after_cancel(self._poll_job)
            except Exception:
                pass
            self._poll_job = None
        safe_grab_release(self)
        if self.winfo_exists():
            self.destroy()

    def _on_save(self):
        if self._poll_job:
            try:
                self.after_cancel(self._poll_job)
            except Exception:
                pass
            self._poll_job = None
        self.app.mtl_config = self._get_draft_config()
        if self.app.mtl_config.use_xuat_cache and getattr(self.app, "xuat_index", None) is None:
            if hasattr(self.app, "_refresh_xuat_index_async"):
                self.app._refresh_xuat_index_async()
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
            text="Include Speaker Names in CSIF headers (@@Speaker / @@_)",
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

        self.worker_queue: queue.Queue = queue.Queue()
        self._req_seq: int = 0
        self._poll_job: Optional[str] = None
        self._comp_widgets: Dict[str, Tuple[tk.Label, ttk.Button]] = {}

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

    def _schedule_poll(self):
        if self._poll_job:
            try:
                self.after_cancel(self._poll_job)
            except Exception:
                pass
            self._poll_job = None
        if self.winfo_exists():
            self._poll_job = self.after(50, self._poll_worker_queue)

    def _poll_worker_queue(self):
        self._poll_job = None
        if not self.winfo_exists():
            return

        try:
            while True:
                msg = self.worker_queue.get_nowait()
                kind = msg[0]
                if kind == "translate_success":
                    _, meta, res = msg
                    file_p, doc_id, b_uid, src_hash, req_seq, eng = meta
                    if (
                        self.winfo_exists()
                        and self.app.current_doc
                        and id(self.app.current_doc) == doc_id
                        and str(self.app.current_file_path or "") == file_p
                        and req_seq == self._req_seq
                    ):
                        b_idx = self.app.current_box_idx
                        if 0 <= b_idx < len(self.app.current_doc.boxes):
                            curr_box = self.app.current_doc.boxes[b_idx]
                            if (
                                _get_box_uid(curr_box) == b_uid
                                and _hash_mtl_source(curr_box.clean_text) == src_hash
                            ):
                                self.txt_trans.delete("1.0", tk.END)
                                self.txt_trans.insert("1.0", res)
                                self.lbl_status.config(text=f"✓ Translated via {eng}")
                elif kind == "translate_error":
                    _, meta, err = msg
                    file_p, doc_id, b_uid, src_hash, req_seq, eng = meta
                    if (
                        self.winfo_exists()
                        and self.app.current_doc
                        and id(self.app.current_doc) == doc_id
                        and req_seq == self._req_seq
                    ):
                        self.lbl_status.config(text=f"❌ Translation failed: {err}")
                elif kind == "fetch_all_result":
                    _, meta, eng, ok, val = msg
                    file_p, doc_id, b_uid, src_hash, req_seq = meta[:5]
                    if (
                        self.winfo_exists()
                        and self.app.current_doc
                        and id(self.app.current_doc) == doc_id
                        and str(self.app.current_file_path or "") == file_p
                        and req_seq == self._req_seq
                    ):
                        b_idx = self.app.current_box_idx
                        if 0 <= b_idx < len(self.app.current_doc.boxes):
                            curr_box = self.app.current_doc.boxes[b_idx]
                            if (
                                _get_box_uid(curr_box) == b_uid
                                and _hash_mtl_source(curr_box.clean_text) == src_hash
                            ):
                                if eng in self._comp_widgets:
                                    lbl_val, btn_use = self._comp_widgets[eng]
                                    if lbl_val.winfo_exists() and btn_use.winfo_exists():
                                        if ok:
                                            fg_panel = best_contrast_fg(self.app.theme["bg_panel"])
                                            lbl_val.config(text=val, fg=fg_panel)
                                            btn_use.config(state="normal", command=lambda r=val: self._use_comp_text(r))
                                        else:
                                            lbl_val.config(text=f"Failed ({val})", fg=self.app.theme.get("accent_yellow", "#f57c00"))
        except queue.Empty:
            pass

        if self.winfo_exists():
            self._schedule_poll()

    def _on_close(self):
        if self._poll_job:
            try:
                self.after_cancel(self._poll_job)
            except Exception:
                pass
            self._poll_job = None
        self.app._translator_dialog = None
        safe_grab_release(self)
        if self.winfo_exists():
            self.destroy()

    def _on_engine_change(self, _event=None):
        self.app.mtl_config.active_engine = self.var_engine.get()
        self.lbl_status.config(text=f"Active engine set to: {self.var_engine.get()}")

    def refresh_box(self):
        if not self.winfo_exists():
            return
        doc = self.app.current_doc
        if not doc or not doc.boxes:
            self.lbl_box_info.config(text="Box 0 / 0")
            self.lbl_speaker.config(text="Speaker: -")
            self.txt_orig.config(state="normal")
            self.txt_orig.delete("1.0", tk.END)
            self.txt_orig.config(state="disabled")
            return

        b_idx = self.app.current_box_idx
        b_idx = max(0, min(b_idx, len(doc.boxes) - 1))
        box = doc.boxes[b_idx]

        self.lbl_box_info.config(text=f"Box {b_idx + 1} / {len(doc.boxes)}")
        self.lbl_speaker.config(text=f"Speaker: {box.speaker or '(None)'}")

        self.txt_orig.config(state="normal")
        self.txt_orig.delete("1.0", tk.END)
        self.txt_orig.insert("1.0", box.clean_text)
        self.txt_orig.config(state="disabled")

        self.txt_trans.delete("1.0", tk.END)
        self.txt_trans.insert("1.0", box.clean_text)
        self.lbl_status.config(text=f"Loaded Box {b_idx + 1}")

    def _on_prev(self):
        self.app.on_prev_box()
        self.refresh_box()

    def _on_next(self):
        self.app.on_next_box()
        self.refresh_box()

    def _on_translate(self):
        doc = self.app.current_doc
        if not doc or not doc.boxes:
            return
        b_idx = self.app.current_box_idx
        if b_idx < 0 or b_idx >= len(doc.boxes):
            return
        box = doc.boxes[b_idx]
        text_to_tr = box.clean_text.strip()
        if not text_to_tr:
            return

        eng = self.var_engine.get()
        self.lbl_status.config(text=f"Translating via {eng}...")

        b_uid = _get_box_uid(box)
        doc_id = id(doc)
        file_p = str(self.app.current_file_path or "")
        src_hash = _hash_mtl_source(text_to_tr)
        self._req_seq += 1
        req_seq = self._req_seq
        meta = (file_p, doc_id, b_uid, src_hash, req_seq, eng)

        q = self.worker_queue

        def on_success(res: str):
            q.put(("translate_success", meta, res))

        def on_error(err: str):
            q.put(("translate_error", meta, str(err)))

        cfg = MTLConfig.from_dict(self.app.mtl_config.to_dict())
        cfg.active_engine = eng

        translate_async(
            text_to_tr,
            cfg,
            on_success=on_success,
            on_error=on_error,
            xuat_cache=getattr(self.app, "xuat_entries", None),
        )
        self._schedule_poll()

    def _on_fetch_all(self):
        doc = self.app.current_doc
        if not doc or not doc.boxes:
            return
        b_idx = self.app.current_box_idx
        if b_idx < 0 or b_idx >= len(doc.boxes):
            return
        box = doc.boxes[b_idx]
        text_to_tr = doc.boxes[b_idx].clean_text.strip()
        if not text_to_tr:
            return

        if not self.comp_frame.winfo_ismapped():
            self.comp_frame.pack(fill="x", padx=14, pady=4, before=self.lbl_status)

        for w in self.comp_frame.winfo_children():
            w.destroy()

        t = self.app.theme
        b_uid = _get_box_uid(box)
        doc_id = id(doc)
        file_p = str(self.app.current_file_path or "")
        src_hash = _hash_mtl_source(text_to_tr)
        self._req_seq += 1
        req_seq = self._req_seq

        self._comp_widgets.clear()
        q = self.worker_queue

        engines_to_query = ["Google", "DeepL", "Local / Sugoi", "LLM / OpenAI", "XUAT Cache"]
        for eng in engines_to_query:
            row = tk.Frame(self.comp_frame, bg=t["bg_panel"])
            row.pack(fill="x", pady=1)

            lbl_name = tk.Label(row, text=f"[{eng}]:", font=("Segoe UI", 8, "bold"), bg=t["bg_panel"], fg=t["misora_pink"], width=14, anchor="w")
            lbl_name.pack(side="left")

            lbl_val = tk.Label(row, text="Fetching...", font=("Segoe UI", 8), bg=t["bg_panel"], fg=t["fg_muted"], anchor="w")
            lbl_val.pack(side="left", fill="x", expand=True)

            btn_use = ttk.Button(row, text="Use", style="Small.TButton", width=4)
            btn_use.pack(side="right")
            btn_use.config(state="disabled")

            self._comp_widgets[eng] = (lbl_val, btn_use)

            meta = (file_p, doc_id, b_uid, src_hash, req_seq, eng)

            def make_worker(engine_name=eng, request_meta=meta):
                def worker():
                    cfg = MTLConfig.from_dict(self.app.mtl_config.to_dict())
                    cfg.active_engine = engine_name
                    engine = MTLEngine(cfg)
                    try:
                        res = engine.translate(text_to_tr, config=cfg, xuat_cache=getattr(self.app, "xuat_entries", None))
                        q.put(("fetch_all_result", request_meta, engine_name, True, res))
                    except Exception as exc:
                        q.put(("fetch_all_result", request_meta, engine_name, False, str(exc)))

                threading.Thread(target=worker, daemon=True).start()

            make_worker()
        self._schedule_poll()

    def _use_comp_text(self, text: str):
        self.txt_trans.delete("1.0", tk.END)
        self.txt_trans.insert("1.0", text)

    def _on_apply(self) -> bool:
        doc = self.app.current_doc
        if not doc or not doc.boxes:
            return False
        b_idx = self.app.current_box_idx
        if b_idx < 0 or b_idx >= len(doc.boxes):
            return False
        if self.app.is_box_locked(b_idx):
            self.app.show_toast(f"🔒 Box {b_idx + 1} is locked against translation.")
            return False

        new_text = self.txt_trans.get("1.0", "end-1c")
        old_box = doc.boxes[b_idx]
        old_sp = old_box.speaker
        old_tx = old_box.clean_text
        box_uid = old_box.uid

        try:
            doc.inject_box(b_idx, old_sp, new_text)
        except Exception as e:
            self.app.logger.exception(f"Failed to apply translation to box {b_idx}:", e)
            self.app.set_status(f"Error applying translation to Box #{b_idx + 1}: {e}", is_error=True)
            return False

        self.app.undo_journal.record(
            BoxEditDelta(
                box_index=b_idx,
                old_speaker=old_sp,
                new_speaker=old_sp,
                old_text=old_tx,
                new_text=new_text,
                file_path=str(self.app.current_file_path) if self.app.current_file_path else "",
                box_uid=box_uid,
                source="mtl",
            )
        )
        self.app._modified_boxes.add(b_idx)
        self.app._mark_document_dirty(self.app.current_file_path)
        self.app._dirty_state_changed()
        self.app._update_views()
        self.app.show_toast(f"✓ Applied translation to Box {b_idx + 1}")
        return True

    def _on_apply_and_next(self):
        if self._on_apply():
            self._on_next()

    def _on_copy(self):
        t = self.txt_trans.get("1.0", tk.END).strip()
        if t:
            self.clipboard_clear()
            self.clipboard_append(t)
            self.app.show_toast("📋 Copied translation to clipboard")


class BatchTranslateDialog(tk.Toplevel):
    """Dialog for automated batch translation of an entire story bundle."""
    def __init__(self, parent: "MisoraApp"):
        super().__init__(parent)
        self.app = parent
        self.title("Batch Translate Story")
        self.geometry("560x420")
        self.minsize(500, 380)
        self.transient(parent)
        self.grab_set()

        t = self.app.theme
        self.configure(bg=t["bg_panel"])
        apply_window_icon(self)

        fg_panel = best_contrast_fg(t["bg_panel"])

        self._cancelled = False
        self._is_running = False
        self._batch_open: bool = False
        self._close_requested: bool = False
        self._poll_job: Optional[str] = None
        self.worker_queue: queue.Queue = queue.Queue()

        content = tk.Frame(self, bg=t["bg_panel"], padx=18, pady=12)
        content.pack(fill="both", expand=True)

        tk.Label(content, text="Batch Translation", font=("Segoe UI", 12, "bold"), bg=t["bg_panel"], fg=t["misora_pink"]).pack(anchor="w", pady=(0, 6))

        # Engine
        r_eng = tk.Frame(content, bg=t["bg_panel"])
        r_eng.pack(fill="x", pady=4)
        tk.Label(r_eng, text="Translation Engine:", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=fg_panel, width=18, anchor="w").pack(side="left")
        self.var_engine = tk.StringVar(master=self, value=self.app.mtl_config.active_engine)
        cb_eng = ttk.Combobox(r_eng, textvariable=self.var_engine, values=MTL_ENGINES, state="readonly", width=18)
        cb_eng.pack(side="left")

        # Scope
        sec_scope = tk.LabelFrame(content, text="Scope & Filter", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"], padx=10, pady=6)
        sec_scope.pack(fill="x", pady=6)

        self.var_scope = tk.StringVar(master=self, value="untranslated")
        tk.Radiobutton(sec_scope, text="Untranslated Only (Contains Japanese characters)", variable=self.var_scope, value="untranslated", bg=t["bg_panel"], fg=fg_panel, selectcolor=t["bg_dark"]).pack(anchor="w")
        tk.Radiobutton(sec_scope, text="All Boxes in Story", variable=self.var_scope, value="all", bg=t["bg_panel"], fg=fg_panel, selectcolor=t["bg_dark"]).pack(anchor="w")
        tk.Radiobutton(sec_scope, text=f"From Current Box ({self.app.current_box_idx + 1}) to End", variable=self.var_scope, value="from_current", bg=t["bg_panel"], fg=fg_panel, selectcolor=t["bg_dark"]).pack(anchor="w")

        # Rate Limit Delay
        r_del = tk.Frame(content, bg=t["bg_panel"])
        r_del.pack(fill="x", pady=4)
        tk.Label(r_del, text="Delay between requests (sec):", bg=t["bg_panel"], fg=fg_panel).pack(side="left")
        self.var_delay = tk.DoubleVar(master=self, value=0.3)
        sp_del = ttk.Spinbox(r_del, from_=0.0, to=5.0, increment=0.1, textvariable=self.var_delay, width=6)
        sp_del.pack(side="left", padx=6)

        # Progress bar
        self.progress = ttk.Progressbar(content, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=(12, 4))

        self.lbl_status = tk.Label(content, text="Ready to start batch translation.", font=("Segoe UI", 9), bg=t["bg_panel"], fg=t["fg_muted"], anchor="w")
        self.lbl_status.pack(fill="x", pady=2)

        # Bottom Buttons
        btn_bar = tk.Frame(self, bg=t["bg_panel"], padx=18, pady=12)
        btn_bar.pack(fill="x", side="bottom")

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.bind("<Escape>", lambda _e=None: self._on_close())

        self.btn_close = ttk.Button(btn_bar, text="Close", style="TButton", command=self._on_close)
        self.btn_close.pack(side="right", padx=4)

        self.btn_start = ttk.Button(btn_bar, text="Start Batch", style="Pink.TButton", command=self._start_batch)
        self.btn_start.pack(side="right", padx=4)

    def _end_undo_batch(self) -> None:
        """Close open undo batch strictly once on the UI main thread (BUG-14)."""
        if getattr(self, "_batch_open", False):
            self._batch_open = False
            try:
                self.app.undo_journal.end_batch()
            except Exception as exc:
                self.app.logger.warning("MTL", f"end_batch error: {exc}")

    def _schedule_poll(self):
        if self._poll_job:
            try:
                self.after_cancel(self._poll_job)
            except Exception:
                pass
            self._poll_job = None
        if self.winfo_exists():
            self._poll_job = self.after(50, self._poll_worker_queue)

    def _on_close(self):
        if self._is_running:
            self._cancelled = True
            self._close_requested = True
            try:
                self.withdraw()
            except Exception:
                pass
            return

        if self._poll_job:
            try:
                self.after_cancel(self._poll_job)
            except Exception:
                pass
            self._poll_job = None

        self._end_undo_batch()
        safe_grab_release(self)
        if self.winfo_exists():
            self.destroy()

    def _start_batch(self):
        doc = self.app.current_doc
        if not doc or not doc.boxes:
            messagebox.showwarning("No Story Open", "Open a story bundle or text file first.")
            return

        jp_regex = re.compile(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]")
        scope = self.var_scope.get()
        targets: List[int] = []
        skipped_locked = 0

        for i, box in enumerate(doc.boxes):
            if scope == "from_current" and i < self.app.current_box_idx:
                continue
            if self.app.is_box_locked(i):
                skipped_locked += 1
                continue
            if scope == "untranslated":
                if jp_regex.search(box.clean_text):
                    targets.append(i)
            else:
                targets.append(i)

        if not targets:
            msg = "No boxes matching selected criteria."
            if skipped_locked > 0:
                msg += f" ({skipped_locked} locked boxes were skipped)"
            self.lbl_status.config(text=msg)
            messagebox.showinfo("Batch Complete", msg)
            return

        self._cancelled = False
        self._is_running = True
        self._close_requested = False
        self.btn_start.config(state="disabled")
        self.progress.config(maximum=len(targets), value=0)

        # Drain any stale messages from queue
        while not self.worker_queue.empty():
            try:
                self.worker_queue.get_nowait()
            except queue.Empty:
                break

        cfg = MTLConfig.from_dict(self.app.mtl_config.to_dict())
        cfg.active_engine = self.var_engine.get()
        delay = float(self.var_delay.get())
        engine = MTLEngine(cfg)
        xuat_cache = getattr(self.app, "xuat_entries", None)

        # Snapshot target box data on UI thread (Rule 15)
        target_inputs = [
            (b_idx, doc.boxes[b_idx].speaker, doc.boxes[b_idx].clean_text)
            for b_idx in targets
        ]

        # Begin undo batch on UI thread before worker thread starts
        self.app.undo_journal.begin_batch(f"Batch Translate ({len(targets)} boxes)")
        self._batch_open = True

        def worker():
            translated_count = 0
            try:
                for step, (b_idx, spk, raw_text) in enumerate(target_inputs):
                    if self._cancelled:
                        break
                    raw_clean = raw_text.strip()
                    if not raw_clean:
                        continue
                    try:
                        res = engine.translate(raw_clean, config=cfg, xuat_cache=xuat_cache)
                        translated_count += 1
                        self.worker_queue.put(("progress", step + 1, b_idx, spk, raw_text, res))
                    except Exception as exc:
                        self.worker_queue.put(("error", step + 1, b_idx, str(exc)))

                    if delay > 0 and step < len(target_inputs) - 1:
                        time.sleep(delay)
            finally:
                self.worker_queue.put(("done", translated_count, skipped_locked))

        threading.Thread(target=worker, daemon=True).start()
        self._schedule_poll()

    def _poll_worker_queue(self):
        self._poll_job = None
        if not self.winfo_exists():
            return
        done_received = False
        final_count = 0
        final_skipped = 0
        try:
            while True:
                msg = self.worker_queue.get_nowait()
                kind = msg[0]
                if kind == "progress":
                    _, step, b_idx, spk, old_tx, new_tx = msg
                    if self.winfo_exists() and not self._close_requested:
                        self.progress.config(value=step)
                        self.lbl_status.config(text=f"Translating Box {b_idx + 1} ({step} / {self.progress['maximum']})...")
                    # Apply on main UI thread (Rule 15)
                    doc = self.app.current_doc
                    if doc and 0 <= b_idx < len(doc.boxes):
                        if not self.app.is_box_locked(b_idx):
                            # Mutate AST first (S07 / BUG-13)
                            doc.inject_box(b_idx, spk, new_tx)
                            self.app.undo_journal.record(
                                BoxEditDelta(
                                    box_index=b_idx,
                                    old_speaker=spk,
                                    new_speaker=spk,
                                    old_text=old_tx,
                                    new_text=new_tx,
                                    file_path=str(self.app.current_file_path or ""),
                                    box_uid=doc.boxes[b_idx].uid,
                                    source="mtl",
                                )
                            )
                            self.app._modified_boxes.add(b_idx)
                elif kind == "error":
                    _, step, b_idx, err_str = msg
                    self.app.logger.warning("MTL", f"Batch translate failed on box {b_idx}: {err_str}")
                elif kind == "done":
                    _, final_count, final_skipped = msg
                    done_received = True
                    break
        except queue.Empty:
            pass

        if done_received:
            self._is_running = False
            self._end_undo_batch()
            if self.app.current_file_path:
                self.app._mark_document_dirty(self.app.current_file_path)
            self.app._dirty_state_changed()
            self.app._update_views()

            if self._close_requested:
                safe_grab_release(self)
                if self.winfo_exists():
                    self.destroy()
                return

            if self.winfo_exists():
                self.btn_start.config(state="normal")
                stat_txt = f"Completed: {final_count} boxes translated."
                toast_txt = f"✓ Batch translated {final_count} boxes"
                if final_skipped > 0:
                    stat_txt += f" ({final_skipped} locked boxes preserved)"
                    toast_txt += f" ({final_skipped} locked boxes preserved)"
                self.lbl_status.config(text=stat_txt)
                self.app.show_toast(toast_txt)
        elif self._is_running or self._close_requested:
            self._schedule_poll()


def main():
    """
    Application entry point.

    Initializes MisoraApp with a fast, lightweight splash screen
    running as a Toplevel of the root application window to avoid
    multi-root Tkinter event loop conflicts and variable orphaning.
    """
    init_process_dpi_awareness()

    initial_file = None
    show_splash = True
    for arg in sys.argv[1:]:
        if arg in ("--no-splash", "-ns"):
            show_splash = False
        elif not arg.startswith("-") and initial_file is None:
            initial_file = arg

    app = MisoraApp(initial_file, show_splash=show_splash)
    app.mainloop()


if __name__ == "__main__":
    main()
