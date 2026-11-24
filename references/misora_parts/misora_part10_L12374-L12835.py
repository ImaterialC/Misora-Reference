# ======================================================================
# FILE: misora.py — PART 10 / 10
# ORIGINAL LINE RANGE : L12374 .. L12835 (total 462 lines of 12835)
# SOURCE SHA-256      : d23baae2be82fe93a18da7d3769af30d19ebe02a8b5f6a3645d56a6f53c0710e
# NOTE FOR AI REVIEWER: Cite ORIGINAL line numbers (L12374..L12835) and symbol names.
# SYMBOLS IN THIS PART (with exact original line numbers):
#   L12374:   TranslatorAssistantDialog._on_close (def)
#   L12380:   TranslatorAssistantDialog._on_engine_change (def)
#   L12384:   TranslatorAssistantDialog.refresh_box (def)
#   L12412:   TranslatorAssistantDialog._on_prev (def)
#   L12416:   TranslatorAssistantDialog._on_next (def)
#   L12420:   TranslatorAssistantDialog._on_translate (def)
#   L12458:   TranslatorAssistantDialog._on_fetch_all (def)
#   L12513:   TranslatorAssistantDialog._use_comp_text (def)
#   L12517:   TranslatorAssistantDialog._on_apply (def)
#   L12560:   TranslatorAssistantDialog._on_apply_and_next (def)
#   L12564:   TranslatorAssistantDialog._on_copy (def)
#   L12572: class BatchTranslateDialog
#   L12574:   BatchTranslateDialog.__init__ (def)
#   L12643:   BatchTranslateDialog._toggle_pin_top (def)
#   L12649:   BatchTranslateDialog._on_close (def)
#   L12665:   BatchTranslateDialog._start_batch (def)
#   L12747:   BatchTranslateDialog._poll_worker_queue (def)
#   L12812: def main()
# ======================================================================

    def _on_close(self):
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
        box = doc.boxes[b_idx]
        text_to_tr = box.clean_text.strip()
        if not text_to_tr:
            return

        eng = self.var_engine.get()
        self.lbl_status.config(text=f"Translating via {eng}...")

        def on_success(res: str):
            def update():
                if self.winfo_exists():
                    self.txt_trans.delete("1.0", tk.END)
                    self.txt_trans.insert("1.0", res)
                    self.lbl_status.config(text=f"✓ Translated via {eng}")
            self.after_idle(update)

        def on_error(err: str):
            def show():
                if self.winfo_exists():
                    self.lbl_status.config(text=f"❌ Translation failed: {err}")
            self.after_idle(show)

        cfg = MTLConfig.from_dict(self.app.mtl_config.to_dict())
        cfg.active_engine = eng

        translate_async(
            text_to_tr,
            cfg,
            on_success=on_success,
            on_error=on_error,
            xuat_cache=getattr(self.app, "xuat_entries", None),
        )

    def _on_fetch_all(self):
        doc = self.app.current_doc
        if not doc or not doc.boxes:
            return
        b_idx = self.app.current_box_idx
        text_to_tr = doc.boxes[b_idx].clean_text.strip()
        if not text_to_tr:
            return

        if not self.comp_frame.winfo_ismapped():
            self.comp_frame.pack(fill="x", padx=14, pady=4, before=self.lbl_status)

        for w in self.comp_frame.winfo_children():
            w.destroy()

        t = self.app.theme
        fg_panel = best_contrast_fg(t["bg_panel"])

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

            def make_worker(engine_name=eng, val_lbl=lbl_val, use_btn=btn_use):
                def worker():
                    cfg = MTLConfig.from_dict(self.app.mtl_config.to_dict())
                    cfg.active_engine = engine_name
                    engine = MTLEngine(cfg)
                    try:
                        res = engine.translate(text_to_tr, config=cfg, xuat_cache=getattr(self.app, "xuat_entries", None))
                        def ok():
                            if self.winfo_exists() and val_lbl.winfo_exists():
                                val_lbl.config(text=res, fg=fg_panel)
                                use_btn.config(state="normal", command=lambda r=res: self._use_comp_text(r))
                        self.after_idle(ok)
                    except Exception as exc:
                        def fail():
                            if self.winfo_exists() and val_lbl.winfo_exists():
                                val_lbl.config(text=f"Failed ({exc})", fg=self.app.theme["accent_yellow"])
                        self.after_idle(fail)

                threading.Thread(target=worker, daemon=True).start()

            make_worker()

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

    def _toggle_pin_top(self):
        self._is_pinned_top = not getattr(self, "_is_pinned_top", False)
        self.wm_attributes("-topmost", self._is_pinned_top)
        self.btn_pin.configure(text="📌" if self._is_pinned_top else "📍")
        self.app.show_toast(f"Translator Assistant {'pinned on top' if self._is_pinned_top else 'unpinned'}")

    def _on_close(self):
        if self._is_running:
            self._cancelled = True
            self._is_running = False
            try:
                self.app.undo_journal.end_batch()
            except Exception:
                pass
            if self.app.current_file_path:
                self.app._mark_document_dirty(self.app.current_file_path)
                self.app._dirty_state_changed()
                self.app._update_views()
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
        self.after(50, self._poll_worker_queue)

    def _poll_worker_queue(self):
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
                    if self.winfo_exists():
                        self.progress.config(value=step)
                        self.lbl_status.config(text=f"Translating Box {b_idx + 1} ({step} / {self.progress['maximum']})...")
                    # Apply on main UI thread (Rule 15)
                    doc = self.app.current_doc
                    if doc and 0 <= b_idx < len(doc.boxes):
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
                        doc.inject_box(b_idx, spk, new_tx)
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
            try:
                self.app.undo_journal.end_batch()
            except Exception:
                pass
            if self.app.current_file_path:
                self.app._mark_document_dirty(self.app.current_file_path)
            if self.winfo_exists():
                self.btn_start.config(state="normal")
                stat_txt = f"Completed: {final_count} boxes translated."
                toast_txt = f"✓ Batch translated {final_count} boxes"
                if final_skipped > 0:
                    stat_txt += f" ({final_skipped} locked boxes preserved)"
                    toast_txt += f" ({final_skipped} locked boxes preserved)"
                self.lbl_status.config(text=stat_txt)
                self.app._dirty_state_changed()
                self.app._update_views()
                self.app.show_toast(toast_txt)
        elif self._is_running:
            self.after(50, self._poll_worker_queue)


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
