# BUNDLE references (14/18) | Files: references/misora_parts/misora_part09_L11634-L13097.py

--- FILE: references/misora_parts/misora_part09_L11634-L13097.py [PART 2 | L1210-1467/1467 | SHA:16619525af33] ---
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

