# BUNDLE references (7/18) | Files: references/misora_parts/misora_part06_L07164-L08651.py

--- FILE: references/misora_parts/misora_part06_L07164-L08651.py [PART 1 | L1-1406/1491 | SHA:5d39497e0feb] ---
# misora.py PART 06/12 | ORIG L7164-L8651/17315 | SHA:ec4d9bfc8ec6
# SYMS: L7164:MisoraApp._get_card_text_widget, L7180:MisoraApp._install_shortcuts_bindtag, L7189:MisoraApp._on_misora_shortcut, L7312:MisoraApp._show_csif_paste_chooser, L7453:MisoraApp._handle_editor_csif_paste, L7471:MisoraApp._bind_shortcuts, L7531:MisoraApp._toggle_continuous_shortcut, L7535:MisoraApp._on_ctrl_h, L7540:MisoraApp._on_ctrl_f, L7545:MisoraApp._on_ctrl_shift_f, L7553:MisoraApp._flush_active_widget, L7603:MisoraApp.open_file, L7823:MisoraApp._update_empty_state_visibility, L7837:MisoraApp._update_views, L8005:MisoraApp._update_raw_view, L8043:MisoraApp._sync_raw_edit_buttons, L8067:MisoraApp._exit_raw_edit_mode, L8077:MisoraApp.on_enter_raw_edit_mode, L8093:MisoraApp.on_cancel_raw_edit_mode, L8099:MisoraApp._parse_and_validate_raw_v2, L8179:MisoraApp._remap_locks_and_jp_keys, L8212:MisoraApp.on_apply_raw_commands, L8306:MisoraApp._flush_continuous_card_edits, L8373:MisoraApp._on_card_text_edited, L8447:MisoraApp._on_card_focus_in, L8460:MisoraApp._clear_card_registry, L8476:MisoraApp._highlight_active_card_header, L8498:MisoraApp._sync_header_controls_for_card, L8532:MisoraApp._copy_single_card_dialogue, L8540:MisoraApp._card_shortcut_wrap, L8552:MisoraApp._highlight_ngui_tags_for_widget, L8566:MisoraApp.on_copy_script, L8581:MisoraApp._on_cont_mousewheel, L8589:MisoraApp._resize_cont_canvas, L8598:MisoraApp._on_toggle_select_box_mode, L8611:MisoraApp._update_dialogue_select_box_ui, L8627:MisoraApp._on_dialogue_box_sel_toggle, L8637:MisoraApp._on_toggle_pin_speaker

    def _get_card_text_widget(self, box_idx: int) -> "tk.Text":
        """Return the card Text widget for box_idx if it exists, else txt_dialogue fallback (S4).

        Guards with winfo_exists() before returning the card widget to avoid stale references
        (STALE-CARD-REGISTRY / Rule 3 widget aliasing guard).
        """
        if hasattr(self, "_card_widgets") and box_idx in self._card_widgets:
            w = self._card_widgets[box_idx].get("txt")
            if w is not None:
                try:
                    if w.winfo_exists():
                        return w
                except Exception:
                    pass
        return self.txt_dialogue

    def _install_shortcuts_bindtag(self, widget: tk.Widget) -> None:
        """Install MisoraShortcuts as the FIRST bindtag on an editor widget (Rule 12)."""
        try:
            current_tags = list(widget.bindtags())
            if "MisoraShortcuts" not in current_tags:
                widget.bindtags(("MisoraShortcuts",) + tuple(current_tags))
        except Exception:
            pass

    def _on_misora_shortcut(self, event: tk.Event) -> Optional[str]:
        """Central shortcut dispatcher on the MisoraShortcuts bindtag (Rule 12)."""
        # 1. Skip if modal grab is active (unless it's self)
        current_grab = self.grab_current()
        if current_grab is not None and current_grab != self:
            return None

        # 2. Skip IME composition / dead keys / empty keysyms
        keysym = getattr(event, "keysym", "")
        if not keysym or keysym.startswith("dead_") or keysym in ("Next_Virtual_Key", "VoidSymbol"):
            return None

        key_lower = keysym.lower()
        state = getattr(event, "state", 0)

        # Modifier bitmasks (Windows Tkinter standard):
        # Shift: 0x0001
        # CapsLock: 0x0002 (mask out)
        # Control: 0x0004
        # Alt: 0x0008 (Mod1) or 0x0020 (Mod3)
        # NumLock: 0x0100 (mask out)
        is_shift = bool(state & 0x0001)
        is_ctrl = bool(state & 0x0004)
        is_alt = bool((state & 0x0008) or (state & 0x0020))

        # 3. Handle explicit Ctrl+Alt application accelerators (X/C/V/A), protect all other keys for AltGr
        if is_ctrl and is_alt:
            if not is_shift:
                if key_lower == "x":
                    self.on_box_cut()
                    return "break"
                elif key_lower == "c":
                    self.on_box_copy()
                    return "break"
                elif key_lower == "v":
                    self.on_box_paste()
                    return "break"
                elif key_lower == "a":
                    self.on_select_whole_story()
                    return "break"
            return None

        # 4. Standard Ctrl+C / Ctrl+X / Ctrl+A: let native widget handlers process them
        if is_ctrl and not is_shift and not is_alt:
            if key_lower in ("c", "x", "a"):
                return None

        # 5. Ctrl+V in editor widget: CSIF detection
        if is_ctrl and not is_shift and not is_alt and key_lower == "v":
            clip_text = self.safe_clipboard_get()
            if clip_text and sniff_format(clip_text) == "csif":
                w = event.widget if isinstance(event.widget, tk.Widget) else self._get_active_text_widget()
                self._handle_editor_csif_paste(w, clip_text)
                return "break"
            return None  # Let standard paste proceed

        # 6. Whitelisted Application Shortcuts (return "break" on match)
        if is_ctrl and not is_alt:
            if not is_shift:
                if key_lower == "h":
                    self.on_show_replace()
                    return "break"
                elif key_lower == "s":
                    self.on_save()
                    return "break"
                elif key_lower == "o":
                    self.on_open_file()
                    return "break"
                elif key_lower == "f":
                    self.on_show_find()
                    return "break"
                elif key_lower == "n":
                    self.on_box_new()
                    return "break"
                elif key_lower == "z":
                    self.on_undo()
                    return "break"
                elif key_lower == "y":
                    self.on_redo()
                    return "break"
                elif key_lower == "t":
                    self.on_open_translator_assistant()
                    return "break"
                elif key_lower == "r":
                    self.on_insert_ruby()
                    return "break"
                elif key_lower == "b":
                    self._shortcut_wrap("[b]", "[/b]")
                    return "break"
                elif key_lower == "i":
                    self._shortcut_wrap("[i]", "[/i]")
                    return "break"
                elif key_lower == "u":
                    self._shortcut_wrap("[u]", "[/u]")
                    return "break"
                elif key_lower == "p":
                    self.on_insert_playername()
                    return "break"
                elif key_lower == "l":
                    self.on_toggle_lock_current_box()
                    return "break"
            else:  # is_shift
                if key_lower == "z":
                    self.on_redo()
                    return "break"
                elif key_lower == "c":
                    self.on_copy_script()
                    return "break"
                elif key_lower == "v":
                    self.on_paste_cross_box()
                    return "break"
                elif key_lower == "t":
                    self.on_copy_ai_prompt()
                    return "break"
                elif key_lower == "i":
                    self.on_import_script()
                    return "break"
                elif key_lower == "e":
                    self.on_export_script()
                    return "break"

        return None

    def _show_csif_paste_chooser(self, clip_text: str) -> Optional[str]:
        """Display modal 4-way chooser dialog when CSIF content is pasted into an editor (Part C.4)."""
        t = self.theme
        dlg = tk.Toplevel(self)
        dlg.title("CSIF Script Detected")
        dlg.transient(self)
        dlg.resizable(False, False)
        dlg.configure(bg=t["bg_panel"])

        choice: List[Optional[str]] = [None]

        def _choose(val: Optional[str]) -> None:
            choice[0] = val
            try:
                dlg.grab_release()
            except Exception:
                pass
            dlg.destroy()

        parsed = parse(clip_text)
        block_count = len(parsed.blocks)
        first_sp = ", ".join(
            (b.speaker if b.speaker else "Narration") for b in parsed.blocks[:3]
        )
        if block_count > 3:
            first_sp += f", ... (+{block_count - 3} more)"

        frame = tk.Frame(dlg, bg=t["bg_panel"], padx=16, pady=14)
        frame.pack(fill="both", expand=True)

        lbl_hdr = tk.Label(
            frame,
            text="Misora CSIF Script Detected in Clipboard",
            font=("Segoe UI", 11, "bold"),
            fg=t["misora_pink"],
            bg=t["bg_panel"],
        )
        lbl_hdr.pack(anchor="w", pady=(0, 6))

        info_txt = (
            f"The clipboard contains {block_count} structured dialogue block(s).\n"
            f"Speakers: {first_sp}\n\n"
            f"Please choose how you would like to apply this clipboard content:"
        )
        lbl_info = tk.Label(
            frame,
            text=info_txt,
            font=("Segoe UI", 9),
            fg=t["fg_text"],
            bg=t["bg_panel"],
            justify="left",
        )
        lbl_info.pack(anchor="w", pady=(0, 12))

        btn_box = tk.Frame(frame, bg=t["bg_panel"])
        btn_box.pack(fill="x", pady=(4, 0))

        btn_ins = tk.Button(
            btn_box,
            text="📥 Insert as New Boxes",
            font=("Segoe UI", 9, "bold"),
            bg=t["highlight_bg"],
            fg=best_contrast_fg(t["highlight_bg"]),
            relief="raised",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: _choose("insert"),
        )
        btn_ins.pack(fill="x", pady=2)

        btn_rep = tk.Button(
            btn_box,
            text="🔄 Paste Across Boxes (Replace)",
            font=("Segoe UI", 9),
            bg=t["bg_editor"],
            fg=t["fg_text"],
            relief="raised",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: _choose("replace"),
        )
        btn_rep.pack(fill="x", pady=2)

        btn_txt = tk.Button(
            btn_box,
            text="📝 Paste as Plain Text",
            font=("Segoe UI", 9),
            bg=t["bg_editor"],
            fg=t["fg_text"],
            relief="raised",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: _choose("text"),
        )
        btn_txt.pack(fill="x", pady=2)

        btn_cancel = tk.Button(
            btn_box,
            text="❌ Cancel",
            font=("Segoe UI", 9),
            bg=t["bg_panel"],
            fg=t["fg_muted"],
            relief="groove",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: _choose(None),
        )
        btn_cancel.pack(fill="x", pady=(4, 0))

        dlg.bind("<Escape>", lambda e: _choose(None))
        dlg.protocol("WM_DELETE_WINDOW", lambda: _choose(None))

        dlg.update_idletasks()
        try:
            pw = self.winfo_width()
            ph = self.winfo_height()
            px = self.winfo_rootx()
            py = self.winfo_rooty()
            dw = dlg.winfo_width()
            dh = dlg.winfo_height()
            dlg.geometry(f"+{px + max(0, (pw - dw) // 2)}+{py + max(0, (ph - dh) // 2)}")
        except Exception:
            pass

        try:
            dlg.grab_set()
            dlg.focus_set()
            self.wait_window(dlg)
        except Exception:
            pass

        return choice[0]

    def _handle_editor_csif_paste(self, widget: tk.Widget, clip_text: str) -> None:
        """Show 4-way chooser dialog when CSIF content is pasted into an editor (Part C.4)."""
        res = self._show_csif_paste_chooser(clip_text)
        if res == "insert":
            self.on_box_paste(confirm=False)
        elif res == "replace":
            self.on_paste_cross_box()
        elif res == "text":
            if isinstance(widget, tk.Text) and widget.winfo_exists():
                try:
                    sel = widget.tag_ranges("sel")
                    if sel:
                        widget.delete(sel[0], sel[1])
                except Exception:
                    pass
                widget.insert(tk.INSERT, clip_text)
                self._commit_widget_edit(widget)

    def _bind_shortcuts(self) -> None:
        self.bind_class("MisoraShortcuts", "<KeyPress>", self._on_misora_shortcut)
        for w in (
            getattr(self, "txt_dialogue", None),
            getattr(self, "entry_speaker", None),
            getattr(self, "txt_continuous", None),
            getattr(self, "txt_box0_summary", None),
            getattr(self, "entry_box0_title", None),
            getattr(self, "entry_box0_subtitle", None),
        ):
            if w is not None:
                self._install_shortcuts_bindtag(w)

        self.bind("<Control-o>", lambda e: self.on_open_file())
        self.bind("<Control-O>", lambda e: self.on_open_folder())
        self.bind("<Control-s>", lambda e: self.on_save())
        self.bind("<Control-q>", lambda e: self._on_app_exit())
        self.bind("<Control-r>", lambda e: self.on_insert_ruby())
        self.bind("<Control-R>", lambda e: self.on_insert_ruby())
        self.bind("<Control-p>", lambda e: self.on_insert_playername())
        self.bind_all("<Control-f>", self._on_ctrl_f)
        self.bind_all("<Control-F>", self._on_ctrl_shift_f)
        self.bind_all("<Control-h>", self._on_ctrl_h)
        self.bind_all("<Control-H>", self._on_ctrl_h)
        self.bind("<Control-z>", lambda e: self.on_undo())
        self.bind("<Control-y>", lambda e: self.on_redo())
        self.bind("<Control-Shift-Z>", lambda e: self.on_redo())
        self.bind("<Control-Shift-z>", lambda e: self.on_redo())
        self.bind("<Control-comma>", lambda e: self._toggle_side_drawer("customize"))
        self.bind("<F1>", lambda e: self._toggle_side_drawer("glossary"))
        self.bind("<F5>", lambda e: self.on_reload())
        self.bind("<F9>", lambda e: self.on_launch_datamine())
        self.bind("<F12>", lambda e: self._toggle_console_shortcut())
        self.bind("<Alt-Left>", lambda e: self.on_prev_box())
        self.bind("<Alt-Right>", lambda e: self.on_next_box())
        self.bind("<Alt-Up>", lambda e: self.on_prev_box())
        self.bind("<Alt-Down>", lambda e: self.on_next_box())
        self.bind("<Control-t>", lambda e: self.on_open_translator_assistant())
        self.bind("<Control-Shift-T>", lambda e: self.on_copy_ai_prompt())
        self.bind("<Control-Shift-t>", lambda e: self.on_copy_ai_prompt())
        self.bind("<Control-Shift-C>", lambda e: self.on_copy_script())
        self.bind("<Control-Shift-c>", lambda e: self.on_copy_script())
        self.bind("<Control-Shift-V>", lambda e: self.on_paste_cross_box())
        self.bind("<Control-Shift-v>", lambda e: self.on_paste_cross_box())
        self.bind("<Control-Shift-I>", lambda e: self.on_import_script())
        self.bind("<Control-Shift-i>", lambda e: self.on_import_script())
        self.bind("<Control-Shift-E>", lambda e: self.on_export_script())
        self.bind("<Control-Shift-e>", lambda e: self.on_export_script())
        self.bind("<Control-l>", lambda e: self.on_toggle_lock_current_box())
        self.bind("<Control-L>", lambda e: self.on_toggle_lock_current_box())
        self.bind("<Control-Alt-x>", lambda e: self.on_box_cut())
        self.bind("<Control-Alt-X>", lambda e: self.on_box_cut())
        self.bind("<Control-Alt-c>", lambda e: self.on_box_copy())
        self.bind("<Control-Alt-C>", lambda e: self.on_box_copy())
        self.bind("<Control-Alt-v>", lambda e: self.on_box_paste())
        self.bind("<Control-Alt-V>", lambda e: self.on_box_paste())
        self.bind("<Control-Alt-a>", lambda e: self.on_select_whole_story())
        self.bind("<Control-Alt-A>", lambda e: self.on_select_whole_story())
        self.bind("<F8>", lambda e: self.on_translate_current_box())

    def _toggle_continuous_shortcut(self) -> None:
        self.var_continuous_view.set(not self.var_continuous_view.get())
        self._on_toggle_continuous_view()

    def _on_ctrl_h(self, _e: Optional[tk.Event] = None) -> str:
        """Bind_all handler for Ctrl+H (Find & Replace bar) returning 'break' (HYG-07)."""
        self.on_show_replace()
        return "break"

    def _on_ctrl_f(self, _e: Optional[tk.Event] = None) -> str:
        """Bind_all handler for Ctrl+F (Find bar) returning 'break'."""
        self.on_show_find()
        return "break"

    def _on_ctrl_shift_f(self, _e: Optional[tk.Event] = None) -> str:
        """Bind_all handler for Ctrl+Shift+F (Find in files) returning 'break'."""
        self.on_show_find_in_files()
        return "break"

    # -------------------------------------------------------------------------
    # Document Loading & Box Display (Page Mode + Continuous Stream Mode)
    # -------------------------------------------------------------------------
    def _flush_active_widget(self) -> bool:
        """Explicitly resolve the active editor widget and commit any pending edits (S1/S3).

        Returns True if flushed cleanly or no active widget, False on commit failure.
        """
        if getattr(self, "current_file_path", None) is None:
            return True

        widget = None
        is_cont = bool(getattr(self, "var_continuous_view", None) and self.var_continuous_view.get())
        cards = getattr(self, "_card_widgets", {})

        if is_cont:
            if getattr(self, "is_box0_active", False) and -1 in cards:
                candidate = cards[-1].get("txt")
                if candidate is not None and candidate.winfo_exists():
                    widget = candidate
            elif getattr(self, "current_box_idx", -1) in cards:
                candidate = cards[self.current_box_idx].get("txt")
                if candidate is not None and candidate.winfo_exists():
                    widget = candidate
            elif getattr(self, "current_doc", None) is None:
                candidate = getattr(self, "txt_continuous", None)
                if candidate is not None and candidate.winfo_exists():
                    widget = candidate
        else:
            if getattr(self, "is_box0_active", False):
                candidate = getattr(self, "txt_box0_summary", None)
                if candidate is not None and candidate.winfo_exists():
                    widget = candidate
            else:
                candidate = getattr(self, "txt_dialogue", None)
                if candidate is not None and candidate.winfo_exists():
                    widget = candidate

        if widget is not None:
            try:
                self._commit_widget_edit(widget)
            except Exception as e:
                self.logger.exception("Failed to flush pending edit:", e)
                messagebox.showerror("Edit Commit Error", f"Could not preserve the current edit:\n{e}")
                return False

        try:
            if hasattr(self, "focus_get") and self.focus_get() == getattr(self, "entry_speaker", None):
                self._commit_speaker_edit()
        except Exception:
            pass
        return True

    def open_file(self, file_path: Union[str, Path], reload_from_disk: bool = False, refresh_ui: bool = True) -> None:
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
        self._exit_raw_edit_mode(refresh=False)

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
            self._original_box_texts = {i: self._original_jp_by_uid.get(_get_box_uid(b), "") for i, b in enumerate(doc.boxes)}
            for b in doc.boxes:
                b_uid = _get_box_uid(b)
                if b_uid is not None:
                    if b_uid not in self._original_jp_by_uid:
                        self._original_jp_by_uid[b_uid] = b.clean_text
                    if hasattr(self, "sync_manager"):
                        self.sync_manager.register_jp_key(b_uid, self._original_jp_by_uid[b_uid])
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
            # Dispose prior UnityPy environment and clear prior entry on reload (BUG-34)
            if reload_from_disk and file_path in self.open_documents:
                prior_entry = self.open_documents.get(file_path)
                if isinstance(prior_entry, dict):
                    if prior_entry.get("env"):
                        dispose_unity_env(prior_entry["env"])
                    prior_entry.clear()
            self.open_documents[file_path] = staged["cache"]
            # Record a fresh saved-state checkpoint for newly loaded documents
            self._record_saved_checkpoint(file_path, staged.get("doc"), staged.get("plain_text", ""))

        if refresh_ui:
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

    def _update_empty_state_visibility(self) -> None:
        """Show centered empty-state frame when 0 documents are open; hide when >=1 document opens."""
        has_docs = bool(self.open_documents) or bool(self.current_doc) or bool(self.current_file_path)
        if not has_docs:
            if hasattr(self, "gd_scroll_wrap") and self.gd_scroll_wrap.winfo_ismapped():
                self.gd_scroll_wrap.pack_forget()
            if hasattr(self, "empty_state_frame") and not self.empty_state_frame.winfo_ismapped():
                self.empty_state_frame.pack(fill="both", expand=True, padx=4, pady=(0, 4))
        else:
            if hasattr(self, "empty_state_frame") and self.empty_state_frame.winfo_ismapped():
                self.empty_state_frame.pack_forget()
            if hasattr(self, "gd_scroll_wrap") and not self.gd_scroll_wrap.winfo_ismapped():
                self.gd_scroll_wrap.pack(fill="both", expand=True, padx=4, pady=(0, 4))

    def _update_views(self) -> None:
        """Update Game Display View (Page or Continuous, Raw or Compiled Preview) and Raw AST View."""
        self._update_empty_state_visibility()
        self._update_dialogue_select_box_ui()
        if hasattr(self, "_sync_raw_edit_buttons"):
            self._sync_raw_edit_buttons()
        compiled = self.var_preview_compiled.get()

        if not self.current_doc:
            self._hide_dialogue_preview_and_restore_editor()
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
            self._refresh_mtl_drawer_box()
            return

        if not self.current_doc.boxes:
            self._hide_dialogue_preview_and_restore_editor()
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
            self._refresh_mtl_drawer_box()
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
                    if hasattr(self, "dialogue_preview_canvas") and self._is_widget_packed(self.dialogue_preview_canvas):
                        self.dialogue_preview_canvas.pack_forget()
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
        if compiled and not self.var_continuous_view.get():
            if hasattr(self, "clean_editor_row") and self._is_widget_packed(self.clean_editor_row):
                self.clean_editor_row.pack_forget()
            if hasattr(self, "ruler_clean") and self._is_widget_packed(self.ruler_clean):
                self.ruler_clean.pack_forget()
            if hasattr(self, "dialogue_preview_canvas") and not self._is_widget_packed(self.dialogue_preview_canvas):
                self.dialogue_preview_canvas.pack(fill="both", expand=True)
        else:
            self._hide_dialogue_preview_and_restore_editor()

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

        if hasattr(self, "btn_prev"):
            can_prev = (self.current_box_idx > 0) or (self.current_doc and self.current_doc.has_metadata())
            self.btn_prev.config(state="normal" if can_prev else "disabled")
        if hasattr(self, "btn_next"):
            self.btn_next.config(state="normal" if self.current_box_idx < total_boxes - 1 else "disabled")

        if self.var_continuous_view.get():
            self._render_continuous_view()
            self._focus_continuous_box(self.current_box_idx, move_cursor=True)
        elif compiled:
            self._render_dialogue_preview_frame(box.speaker, box.clean_text)
            self.gd_canvas.yview_moveto(0.0)
            self.gd_inner.update_idletasks()
            self._sync_gd_scroll_bounds()
        else:
            self.txt_dialogue.config(state="normal")
            self.txt_dialogue.delete("1.0", tk.END)
            self.txt_dialogue.insert("1.0", box.clean_text)
            self._highlight_ngui_tags()
            self._highlight_dialogue_matches()
            self._highlight_secret_whitespace(self.txt_dialogue)
            self._update_gutter_clean()
            self.gd_canvas.yview_moveto(0.0)
            self._auto_resize_dialogue_box()

        self._update_raw_view()
        self._refresh_mtl_drawer_box()
        if hasattr(self, "_translator_dialog") and self._translator_dialog and self._translator_dialog.winfo_exists():
            self._translator_dialog.refresh_box()

    def _update_raw_view(self) -> None:
        """Render Raw AST View and highlight records associated with current_box_idx or Box 0."""
        if getattr(self, "_raw_edit_mode", False):
            return
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

    def _sync_raw_edit_buttons(self) -> None:
        """Sync visibility and enabled state of Raw Commands edit/apply/cancel buttons."""
        in_edit = bool(getattr(self, "_raw_edit_mode", False))
        has_doc = self.current_doc is not None
        if hasattr(self, "btn_edit_raw") and self.btn_edit_raw.winfo_exists():
            if in_edit:
                self.btn_edit_raw.pack_forget()
            else:
                self.btn_edit_raw.config(state="normal" if has_doc else "disabled")
                if not self.btn_edit_raw.winfo_manager():
                    self.btn_edit_raw.pack(side="right", padx=(4, 0))
        if hasattr(self, "btn_apply_raw") and self.btn_apply_raw.winfo_exists():
            if in_edit:
                if not self.btn_apply_raw.winfo_manager():
                    self.btn_apply_raw.pack(side="right", padx=(4, 0))
            else:
                self.btn_apply_raw.pack_forget()
        if hasattr(self, "btn_cancel_raw") and self.btn_cancel_raw.winfo_exists():
            if in_edit:
                if not self.btn_cancel_raw.winfo_manager():
                    self.btn_cancel_raw.pack(side="right", padx=(4, 0))
            else:
                self.btn_cancel_raw.pack_forget()

    def _exit_raw_edit_mode(self, refresh: bool = True) -> None:
        """Exit Raw Commands edit mode cleanly and restore read-only state (BUG-37)."""
        self._raw_edit_mode = False
        if hasattr(self, "txt_raw") and self.txt_raw.winfo_exists():
            self.txt_raw.config(state="disabled")
        if hasattr(self, "_sync_raw_edit_buttons"):
            self._sync_raw_edit_buttons()
        if refresh:
            self._update_raw_view()

    def on_enter_raw_edit_mode(self) -> None:
        """Enter whole-file lossless v2 editing mode in Raw Commands (FEAT-11)."""
        if not self.current_doc:
            self.show_toast("No story document loaded")
            return
        self._flush_active_widget()
        self._raw_edit_mode = True
        self.txt_raw.config(state="normal")
        self.txt_raw.delete("1.0", tk.END)
        self.txt_raw.insert("1.0", self.current_doc.to_v2_text())
        self._sync_raw_edit_buttons()
        if hasattr(self, "lbl_status") and self.lbl_status.winfo_exists():
            self.lbl_status.config(
                text="Raw Commands Edit Mode (v2) — click Apply Raw to commit or Revert / Cancel to discard."
            )

    def on_cancel_raw_edit_mode(self) -> None:
        """Discard Raw Commands v2 edits and return to read-only view."""
        self._exit_raw_edit_mode(refresh=True)
        if hasattr(self, "lbl_status") and self.lbl_status.winfo_exists():
            self.lbl_status.config(text="Raw Commands edit cancelled.")

    @staticmethod
    def _parse_and_validate_raw_v2(v2_text: str) -> StoryDocument:
        """Parse and structurally validate lossless v2 text via binary round-trip (NO-07, DEF-02)."""
        if not isinstance(v2_text, str) or not v2_text.strip():
            raise ValueError("Raw Commands v2 text is empty.")

        lines = [l.rstrip("\r\n") for l in v2_text.splitlines()]
        if lines and lines[0].startswith("#!priconne-story"):
            lines.pop(0)

        from core.story_ast import DEFAULT_CATEGORIES  # local import to avoid top-level churn

        i = 0
        has_record_blocks = False
        while i < len(lines):
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines):
                break
            has_record_blocks = True
            header = lines[i].strip()
            i += 1

            if "#" in header:
                _cmd_name, cid_str = header.split("#", 1)
                if not cid_str.isdigit():
                    raise ValueError(f"Invalid numeric command ID in header '{header}'.")
                cid = int(cid_str)
                if not (0 <= cid <= 65535):
                    raise ValueError(f"Command ID {cid} out of uint16 range (0..65535) in '{header}'.")
            elif header.startswith("cmd_"):
                cid_str = header[4:]
                if not cid_str.isdigit():
                    raise ValueError(f"Invalid numeric command header '{header}'.")
                cid = int(cid_str)
                if not (0 <= cid <= 65535):
                    raise ValueError(f"Command ID {cid} out of uint16 range (0..65535) in '{header}'.")
            else:
                if header not in _AST_INV_CMD_MAP:
                    raise ValueError(f"Unknown command name '{header}' without explicit #<id>.")

            while i < len(lines):
                l = lines[i]
                i += 1
                if not l.strip():
                    break
                if l in DEFAULT_CATEGORIES and not l.startswith("\\"):
                    break
                if l.startswith("\\b64:"):
                    _ast_unescape_arg(l)

        if not has_record_blocks:
            raise ValueError("Raw Commands v2 text contains no command records.")

        candidate = StoryDocument.from_v2_text(v2_text)
        if not candidate.records:
            raise ValueError("Parsed v2 document contains zero records.")

        for idx, rec in enumerate(candidate.records):
            if not (0 <= rec.cmd_id <= 65535):
                raise ValueError(f"Record {idx} ({rec.cmd_name}) has out-of-range cmd_id {rec.cmd_id}.")

        binary_bytes = candidate.to_binary()
        roundtrip = StoryDocument.from_binary(binary_bytes)
        if len(roundtrip.records) != len(candidate.records):
            raise ValueError(
                f"Binary round-trip record count mismatch ({len(roundtrip.records)} != {len(candidate.records)})."
            )
        for idx, (orig_r, rt_r) in enumerate(zip(candidate.records, roundtrip.records)):
            if orig_r.cmd_id != rt_r.cmd_id:
                raise ValueError(
                    f"Binary round-trip cmd_id mismatch at record {idx}: {rt_r.cmd_id} != {orig_r.cmd_id}."
                )
            expected_args = [a if a != "" else " " for a in orig_r.args]
            if rt_r.args != expected_args:
                raise ValueError(
                    f"Binary round-trip argument parity mismatch at record {idx} ({orig_r.cmd_name})."
                )
        return candidate

    def _remap_locks_and_jp_keys(
        self,
        stable_locks: List[Tuple[int, str]],
        old_jp_by_ordinal: Dict[int, str],
        old_clean_by_ordinal: Dict[int, str],
    ) -> None:
        """Remap _original_jp_by_uid and _locked_box_uids via stable composite keys (CLAUDE-N02)."""
        new_jp_by_uid: Dict[int, str] = {}
        if self.current_doc and self.current_doc.boxes:
            for i, box in enumerate(self.current_doc.boxes):
                new_uid = _get_box_uid(box)
                if new_uid is None:
                    continue
                if i in old_jp_by_ordinal and box.clean_text == old_clean_by_ordinal.get(i):
                    new_jp_by_uid[new_uid] = old_jp_by_ordinal[i]
                else:
                    new_jp_by_uid[new_uid] = box.clean_text

        matched_uids, _unresolved = restore_stable_locks(self.current_doc, stable_locks, new_jp_by_uid)
        self._locked_box_uids = set(matched_uids)
        self._original_jp_by_uid = new_jp_by_uid

        if hasattr(self, "sync_manager") and self.sync_manager is not None:
            for b_uid, jp_txt in new_jp_by_uid.items():
                self.sync_manager.register_jp_key(b_uid, jp_txt)

        if self.current_file_path:
            cur_p = Path(self.current_file_path).resolve()
            if cur_p in self.open_documents:
                self.open_documents[cur_p]["locked_box_uids"] = set(self._locked_box_uids)
                self.open_documents[cur_p]["original_jp_by_uid"] = dict(self._original_jp_by_uid)
        self._resync_box_indices_from_uids()

    def on_apply_raw_commands(self) -> None:
        """Confirm, validate, and atomically commit whole-file Raw Commands v2 edits (FEAT-11)."""
        if not self.current_doc:
            return
        confirmed = messagebox.askyesno(
            "Apply Raw Commands",
            "Applying Raw Commands will replace all workspace records for the current document.\n\n"
            "Do you want to validate and apply these changes?",
            parent=self,
        )
        if not confirmed:
            return

        raw_text = self.txt_raw.get("1.0", "end-1c")
        try:
            candidate = self._parse_and_validate_raw_v2(raw_text)
        except Exception as exc:
            self._exit_raw_edit_mode(refresh=True)
            messagebox.showerror(
                "Raw Commands Validation Error",
                f"Failed to parse or validate Raw Commands v2 script:\n\n{exc}\n\n"
                "No changes were applied; Raw Commands has been reverted.",
                parent=self,
            )
            if hasattr(self, "lbl_status") and self.lbl_status.winfo_exists():
                self.lbl_status.config(text=f"Raw Commands error: {exc}")
            return

        # Snapshot pre-edit state before mutating
        old_records = copy.deepcopy(self.current_doc.records)
        old_removed = set(self.current_doc.removed_records)
        old_box_idx = int(getattr(self, "current_box_idx", 0))
        old_is_box0 = bool(getattr(self, "is_box0_active", False))
        old_locked_uids = set(getattr(self, "_locked_box_uids", set()))
        old_jp_by_uid = dict(getattr(self, "_original_jp_by_uid", {}))

        stable_locks = get_document_stable_locks(self.current_doc, old_locked_uids, old_jp_by_uid)
        old_jp_by_ordinal = {
            i: old_jp_by_uid.get(_get_box_uid(b), b.clean_text)
            for i, b in enumerate(self.current_doc.boxes)
        }
        old_clean_by_ordinal = {i: b.clean_text for i, b in enumerate(self.current_doc.boxes)}

        # Mutate AST & rebuild Box projection
        self.current_doc.records = copy.deepcopy(candidate.records)
        self.current_doc.removed_records = set()
        self.current_doc._rebuild_boxes()

        # Remap stable locks & immutable JP keys
        self._remap_locks_and_jp_keys(stable_locks, old_jp_by_ordinal, old_clean_by_ordinal)

        # Clamp cursor bounds safely
        if self.current_doc.boxes:
            self.current_box_idx = max(0, min(old_box_idx, len(self.current_doc.boxes) - 1))
        else:
            self.current_box_idx = 0
        self.is_box0_active = bool(old_is_box0 and self.current_doc.has_metadata())

        new_records = copy.deepcopy(self.current_doc.records)
        new_locked_uids = set(getattr(self, "_locked_box_uids", set()))
        new_jp_by_uid = dict(getattr(self, "_original_jp_by_uid", {}))

        # Record single atomic DocumentRecordsDelta
        self.undo_journal.record(
            DocumentRecordsDelta(
                file_path=str(self.current_file_path or ""),
                old_records=old_records,
                new_records=new_records,
                old_removed_records=old_removed,
                new_removed_records=set(),
                old_box_idx=old_box_idx,
                new_box_idx=self.current_box_idx,
                old_is_box0=old_is_box0,
                new_is_box0=self.is_box0_active,
                old_locked_uids=old_locked_uids,
                new_locked_uids=new_locked_uids,
                old_jp_by_uid=old_jp_by_uid,
                new_jp_by_uid=new_jp_by_uid,
            ),
            label="Edit Raw Commands",
        )

        self._mark_document_dirty(self.current_file_path)
        self._exit_raw_edit_mode(refresh=False)
        self._update_views()
        self._sync_clean_view_to_current_box()
        self._dirty_state_changed()
        if hasattr(self, "lbl_status") and self.lbl_status.winfo_exists():
            self.lbl_status.config(text="Applied Raw Commands v2 changes.")
        self.logger.info("Edit", "Applied Raw Commands v2 edits.")

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
                self._apply_gutter_overflow_tag(gutter)
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
        """Syntax-color NGUI tags and pixel-calibrated overflow within a specific Text widget."""
        if not w.winfo_exists():
            return
        if self.var_preview_compiled.get():
            self._apply_overflow_highlights(w)
            return
        w.tag_remove("ngui_tag", "1.0", tk.END)
        tx = w.get("1.0", "end-1c")
        for m in NGUI_TAG_RE.finditer(tx):
            w.tag_add("ngui_tag", f"1.0 + {m.start()}c", f"1.0 + {m.end()}c")
        self._apply_overflow_highlights(w)
        w.tag_raise("ngui_tag")

    def on_copy_script(self) -> None:

