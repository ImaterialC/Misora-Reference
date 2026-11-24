# ======================================================================
# FILE: misora.py — PART 02 / 10
# ORIGINAL LINE RANGE : L1496 .. L2880 (total 1385 lines of 12835)
# SOURCE SHA-256      : d23baae2be82fe93a18da7d3769af30d19ebe02a8b5f6a3645d56a6f53c0710e
# NOTE FOR AI REVIEWER: Cite ORIGINAL line numbers (L1496..L2880) and symbol names.
# SYMBOLS IN THIS PART (with exact original line numbers):
#   L01496:   MisoraApp._install_exception_hooks (def)
#   L01505:   MisoraApp.report_callback_exception (def)
#   L01514:   MisoraApp._on_app_exit (def)
#   L01549:   MisoraApp._on_root_destroy (def)
#   L01572:   MisoraApp.destroy (def)
#   L01630:   MisoraApp._load_user_prefs (def)
#   L01739:   MisoraApp._save_user_prefs (def)
#   L01796:   MisoraApp._detect_active_preset_name (def)
#   L01803:   MisoraApp._is_dark_color (def)
#   L01808:   MisoraApp._is_light_theme (def)
#   L01812:   MisoraApp._shift_hex (def)
#   L01822:   MisoraApp._tag_role (def)
#   L01827:   MisoraApp._apply_theme_and_fonts_live (def)
#   L02114:   MisoraApp.set_status (def)
#   L02145:   MisoraApp._reset_status (def)
#   L02158:   MisoraApp.show_toast (def)
#   L02197:   MisoraApp._display_toast (def)
#   L02254:   MisoraApp._dismiss_toast (def)
#   L02277:   MisoraApp._configure_editor_rich_tags (def)
#   L02318:   MisoraApp._init_drag_and_drop (def)
#   L02430:   MisoraApp._cleanup_drag_and_drop (def)
#   L02453:   MisoraApp.on_force_open_file (def)
#   L02463:   MisoraApp._check_batch_safety (def)
#   L02504:   MisoraApp._on_dnd_settings_dialog (def)
#   L02594:   MisoraApp._handle_dropped_paths (def)
#   L02677:   MisoraApp._process_opened_folder (def)
#   L02782:   MisoraApp._set_project_folder (def)
#   L02790:   MisoraApp._resolve_xuat_text_root (def)
#   L02804:   MisoraApp._resolve_project_search_roots (def)
#   L02841:   MisoraApp._detect_environment (def)
#   L02871:   MisoraApp._get_backup_dir (def)
# ======================================================================

    def _install_exception_hooks(self) -> None:
        def _sys_excepthook(exc_type, exc_value, exc_tb):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_tb)
                return
            self.logger.exception("Unhandled Python exception:", exc_value)

        sys.excepthook = _sys_excepthook

    def report_callback_exception(self, exc, val, tb) -> None:  # type: ignore[override]
        self.logger.exception("Unhandled Tkinter callback exception:", val)
        try:
            err_msg = f"Error: {val}"
            self.set_status(err_msg, is_error=True)
            self.show_toast(err_msg, duration_ms=4000, is_accent=False, is_error=True, status_bar=False)
        except Exception:
            pass

    def _on_app_exit(self) -> None:
        """Save configuration cleanly on window close and exit (S3).

        Prompts Save/Discard/Cancel per dirty document.
        Aborts exit if Cancel is chosen or if any save fails.
        """
        if not self._flush_active_widget():
            return

        dirty_paths = [
            p for p, d in list(self.open_documents.items())
            if (p == self.current_file_path and self.is_dirty) or d.get("dirty")
        ]
        if self.current_file_path and self.is_dirty:
            cur_p = Path(self.current_file_path).resolve()
            if cur_p not in [p.resolve() for p in dirty_paths]:
                dirty_paths.append(cur_p)

        for p in dirty_paths:
            ans = messagebox.askyesnocancel(
                "Unsaved Changes",
                f"'{p.name}' has unsaved changes.\nSave before exiting?",
                parent=self,
            )
            if ans is None:
                return
            if ans:
                if not self._save_document_entry(p):
                    return

        self.logger.info("UI / Theme / Config", "Saving configuration on exit...")
        self._save_user_prefs(silent=True)
        self._cleanup_drag_and_drop()
        self.destroy()

    def _on_root_destroy(self, event: tk.Event) -> None:
        if event.widget is self:
            self._destroyed = True
            if hasattr(self, "_search_poll_job") and self._search_poll_job:
                try:
                    self.after_cancel(self._search_poll_job)
                except Exception:
                    pass
                self._search_poll_job = None
            if hasattr(self, "_toast_after_id") and self._toast_after_id:
                try:
                    self.after_cancel(self._toast_after_id)
                except Exception:
                    pass
                self._toast_after_id = None
            if hasattr(self, "_status_after_id") and self._status_after_id:
                try:
                    self.after_cancel(self._status_after_id)
                except Exception:
                    pass
                self._status_after_id = None
            self._cleanup_drag_and_drop()

    def destroy(self) -> None:
        self._destroyed = True
        if hasattr(self, "_search_poll_job") and self._search_poll_job:
            try:
                self.after_cancel(self._search_poll_job)
            except Exception:
                pass
            self._search_poll_job = None
        if hasattr(self, "_toast_after_id") and self._toast_after_id:
            try:
                self.after_cancel(self._toast_after_id)
            except Exception:
                pass
            self._toast_after_id = None
        if hasattr(self, "_status_after_id") and self._status_after_id:
            try:
                self.after_cancel(self._status_after_id)
            except Exception:
                pass
            self._status_after_id = None
        if hasattr(self, "_toast_queue"):
            self._toast_queue.clear()
        if hasattr(self, "_toast_widget") and self._toast_widget:
            try:
                self._toast_widget.destroy()
            except Exception:
                pass
            self._toast_widget = None
        self._toast_active = False

        for job_attr in ("_cont_resize_job", "_eyedropper_after_id"):
            if hasattr(self, job_attr):
                job_id = getattr(self, job_attr)
                if job_id:
                    try:
                        self.after_cancel(job_id)
                    except Exception:
                        pass
                    setattr(self, job_attr, None)

        # S8b-2: Dispose all open document environments and prune icon cache
        try:
            for entry in list(getattr(self, "open_documents", {}).values()):
                if isinstance(entry, dict) and entry.get("env"):
                    dispose_unity_env(entry["env"])
            if getattr(self, "current_unity_env", None):
                dispose_unity_env(self.current_unity_env)
                self.current_unity_env = None
            prune_icon_cache(self)
        except Exception:
            pass

        self._cleanup_drag_and_drop()
        super().destroy()

    # -------------------------------------------------------------------------
    # Persistent Preferences & Contrast-Safe Theme Helpers (#2 & #13)
    # -------------------------------------------------------------------------
    def _load_user_prefs(self) -> Dict[str, Any]:
        """Load saved font, theme & debug settings from misora_config.json."""
        merged_theme = dict(DEFAULT_PREFS["theme"])
        merged_debug: Dict[str, Any] = {
            "console_visible": False,
            "log_to_file": False,
            "level": "Info",
            "categories": {cat: True for cat in LOG_CATEGORIES},
        }
        prefs: Dict[str, Any] = {
            "dialogue_font_family": DEFAULT_PREFS["dialogue_font_family"],
            "dialogue_font_size": DEFAULT_PREFS["dialogue_font_size"],
            "raw_font_size": DEFAULT_PREFS["raw_font_size"],
            "ui_font_size": DEFAULT_PREFS["ui_font_size"],
            "theme": merged_theme,
            "debug": merged_debug,
        }
        if CONFIG_PATH.is_file():
            try:
                raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    if isinstance(raw.get("dialogue_font_family"), str) and raw["dialogue_font_family"].strip():
                        prefs["dialogue_font_family"] = raw["dialogue_font_family"].strip()
                    for k, lo, hi in (
                        ("dialogue_font_size", 8, 28),
                        ("raw_font_size", 7, 22),
                        ("ui_font_size", 8, 16),
                    ):
                        val = raw.get(k)
                        if isinstance(val, int) and not isinstance(val, bool) and lo <= val <= hi:
                            prefs[k] = val
                    saved_theme = raw.get("theme")
                    if isinstance(saved_theme, dict):
                        for tk_key in merged_theme:
                            hv = saved_theme.get(tk_key)
                            if isinstance(hv, str) and HEX_COLOR_RE.match(hv.strip()):
                                merged_theme[tk_key] = hv.strip().lower()
                    saved_dbg = raw.get("debug")
                    if isinstance(saved_dbg, dict):
                        if isinstance(saved_dbg.get("console_visible"), bool):
                            merged_debug["console_visible"] = saved_dbg["console_visible"]
                        if isinstance(saved_dbg.get("log_to_file"), bool):
                            merged_debug["log_to_file"] = saved_dbg["log_to_file"]
                        if saved_dbg.get("level") in LOG_LEVELS:
                            merged_debug["level"] = saved_dbg["level"]
                        scats = saved_dbg.get("categories")
                        if isinstance(scats, dict):
                            for cat in LOG_CATEGORIES:
                                if cat == ALWAYS_ON_CATEGORY:
                                    merged_debug["categories"][cat] = True
                                elif isinstance(scats.get(cat), bool):
                                    merged_debug["categories"][cat] = scats[cat]
                self.logger.debug("UI / Theme / Config", f"Loaded config from {CONFIG_PATH}")
                # Load Step 3-4 path/dock config (additive; no version bump needed)
                def _load_path(key: str) -> Optional[Path]:
                    v = raw.get(key)
                    return Path(v) if isinstance(v, str) and v else None
                self.backup_folder = _load_path("backup_folder")
                self.project_folder = _load_path("project_folder") or _load_path("bepinex_project_folder")
                self.bepinex_project_folder = self.project_folder
                self.datamine_exe = _load_path("datamine_exe")
                self.external_editor_path = _load_path("external_editor_path")
                self.notepadpp_path = _load_path("notepadpp_path")
                self.last_opened_dir = _load_path("last_opened_dir")
                self.selected_search_folder = _load_path("selected_search_folder")
                if isinstance(raw.get("saved_opened_files"), list):
                    self._saved_opened_files = [Path(p) for p in raw["saved_opened_files"] if isinstance(p, str) and p and Path(p).exists()]
                else:
                    self._saved_opened_files = []
                self._saved_active_file = _load_path("saved_active_file")
                if isinstance(raw.get("recent_files"), list):
                    self.recent_files = [Path(p) for p in raw["recent_files"] if isinstance(p, str) and p and Path(p).exists()]
                else:
                    self.recent_files = []
                if isinstance(raw.get("left_dock_tab"), str):
                    self._left_dock_tab = raw["left_dock_tab"]
                if isinstance(raw.get("left_dock_width"), int):
                    self._left_dock_width = max(140, min(600, raw["left_dock_width"]))
                if isinstance(raw.get("datamine_confirm_skip"), bool):
                    self._datamine_confirm_skip = raw["datamine_confirm_skip"]
                if isinstance(raw.get("show_line_numbers"), bool):
                    self.show_line_numbers = raw["show_line_numbers"]
                if isinstance(raw.get("show_column_ruler"), bool):
                    self.show_column_ruler = raw["show_column_ruler"]
                if isinstance(raw.get("mtl"), dict):
                    self.mtl_config = MTLConfig.from_dict(raw["mtl"])
                if isinstance(raw.get("dnd_batch_threshold"), int):
                    self.dnd_batch_threshold = max(0, raw["dnd_batch_threshold"])
                if isinstance(raw.get("dnd_size_threshold_mb"), (int, float)):
                    self.dnd_size_threshold_mb = max(0.0, float(raw["dnd_size_threshold_mb"]))
                if isinstance(raw.get("dnd_filter_binary"), bool):
                    self.dnd_filter_binary = raw["dnd_filter_binary"]
                if isinstance(raw.get("window_geometry"), str) and raw["window_geometry"].strip():
                    self._saved_geometry = raw["window_geometry"].strip()
                if isinstance(raw.get("continuous_view"), bool):
                    self._saved_continuous_view = raw["continuous_view"]
                if isinstance(raw.get("sync_xuat"), bool):
                    self._saved_sync_xuat = raw["sync_xuat"]
            except Exception as exc:
                self.logger.warning("UI / Theme / Config", f"Failed to parse {CONFIG_PATH}: {exc}")
                try:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    bak_path = CONFIG_PATH.parent / f"misora_config.bak_{ts}.json"
                    shutil.copy2(CONFIG_PATH, bak_path)
                    self.logger.info("UI / Theme / Config", f"Preserved corrupt config as {bak_path}")
                except Exception as bak_err:
                    self.logger.error("UI / Theme / Config", f"Failed to preserve corrupt config: {bak_err}")
        return prefs

    def _save_user_prefs(self, silent: bool = False) -> None:
        """Atomically persist current font, theme, path & MTL preferences to misora_config.json."""
        try:
            dbg_snapshot = self.logger.get_config_snapshot()
            dbg_snapshot["console_visible"] = (
                bool(self.var_console_visible.get())
                if hasattr(self, "var_console_visible")
                else self._console_visible
            )
            self.prefs["debug"] = dbg_snapshot

            payload = {
                "config_version": 4,
                "dialogue_font_family": str(self.prefs["dialogue_font_family"]),
                "dialogue_font_size": int(self.prefs["dialogue_font_size"]),
                "raw_font_size": int(self.prefs["raw_font_size"]),
                "ui_font_size": int(self.prefs["ui_font_size"]),
                "theme": dict(self.theme),
                "debug": dbg_snapshot,
                # Path & dock state
                "backup_folder": str(self.backup_folder) if self.backup_folder else "",
                "project_folder": str(self.project_folder) if getattr(self, "project_folder", None) else (str(self.bepinex_project_folder) if getattr(self, "bepinex_project_folder", None) else ""),
                "bepinex_project_folder": str(self.bepinex_project_folder) if getattr(self, "bepinex_project_folder", None) else (str(self.project_folder) if getattr(self, "project_folder", None) else ""),
                "datamine_exe": str(self.datamine_exe) if self.datamine_exe else "",
                "external_editor_path": str(self.external_editor_path) if self.external_editor_path else "",
                "notepadpp_path": str(self.notepadpp_path) if self.notepadpp_path else "",
                "last_opened_dir": str(self.last_opened_dir) if getattr(self, "last_opened_dir", None) else "",
                "selected_search_folder": str(self.selected_search_folder) if getattr(self, "selected_search_folder", None) else "",
                "saved_opened_files": [str(p) for p in getattr(self, "open_documents", {}).keys() if p.exists()],
                "saved_active_file": str(self.current_file_path) if getattr(self, "current_file_path", None) and self.current_file_path.exists() else "",
                "recent_files": [str(p) for p in getattr(self, "recent_files", [])[:15] if isinstance(p, Path) and p.exists()],
                "left_dock_tab": self._left_dock_tab if hasattr(self, "_left_dock_tab") else "search",
                "left_dock_width": self._left_dock_width if hasattr(self, "_left_dock_width") else 340,
                "datamine_confirm_skip": self._datamine_confirm_skip if hasattr(self, "_datamine_confirm_skip") else False,
                # Line numbers & rulers
                "show_line_numbers": bool(self.var_show_line_numbers.get()) if hasattr(self, "var_show_line_numbers") else self.show_line_numbers,
                "show_column_ruler": bool(self.var_show_column_ruler.get()) if hasattr(self, "var_show_column_ruler") else self.show_column_ruler,
                # MTL translation configuration (Rule 17: DPAPI encrypted secrets on disk)
                "mtl": self.mtl_config.to_dict(secure=True) if hasattr(self, "mtl_config") else {},
                # Drag & Drop safety configuration
                "dnd_batch_threshold": getattr(self, "dnd_batch_threshold", 10),
                "dnd_size_threshold_mb": getattr(self, "dnd_size_threshold_mb", 25.0),
                "dnd_filter_binary": getattr(self, "dnd_filter_binary", True),
                # Window geometry & view toggles (Bug #2)
                "window_geometry": self.geometry() if hasattr(self, "geometry") else "",
                "continuous_view": bool(self.var_continuous_view.get()) if hasattr(self, "var_continuous_view") else False,
                "sync_xuat": bool(self.var_sync_xuat.get()) if hasattr(self, "var_sync_xuat") else True,
            }
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = CONFIG_PATH.with_suffix(".json.tmp")
            tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            os.replace(tmp_path, CONFIG_PATH)
            if not silent:
                self.logger.debug("UI / Theme / Config", f"Saved config to {CONFIG_PATH}")
        except Exception as e:
            self.logger.error("UI / Theme / Config", f"Failed to save config '{CONFIG_PATH}': {e}")

    def _detect_active_preset_name(self) -> str:
        """Return matching preset name if current theme equals a preset, else 'Custom'."""
        for name, preset in THEME_PRESETS.items():
            if all(self.theme.get(k, "").lower() == v.lower() for k, v in preset.items()):
                return name
        return "Custom"

    @staticmethod
    def _is_dark_color(hex_color: str) -> bool:
        """Return True if a #RRGGBB color has low WCAG relative luminance."""
        return wcag_relative_luminance(hex_color) < 0.179

    def _is_light_theme(self) -> bool:
        """Return True if current active theme panel background is light."""
        return not self._is_dark_color(self.theme.get("bg_panel", "#ffffff"))

    @staticmethod
    def _shift_hex(hex_color: str, delta: int) -> str:
        """Lighten or darken a #RRGGBB color by `delta` per channel."""
        if not HEX_COLOR_RE.match(hex_color):
            return hex_color
        r = max(0, min(255, int(hex_color[1:3], 16) + delta))
        g = max(0, min(255, int(hex_color[3:5], 16) + delta))
        b = max(0, min(255, int(hex_color[5:7], 16) + delta))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _tag_role(self, widget: tk.Widget, role: str) -> tk.Widget:
        """Attach a semantic theme role to a Tk widget for live re-theming."""
        setattr(widget, "_misora_role", role)
        return widget

    def _apply_theme_and_fonts_live(self, save: bool = True) -> None:
        """Re-apply current theme colors (with WCAG contrast) and font sizes across all active widgets."""
        THEME.update(self.theme)
        self._apply_styles()

        t = self.theme
        d_fam = self.prefs["dialogue_font_family"]
        d_sz = int(self.prefs["dialogue_font_size"])
        r_sz = int(self.prefs["raw_font_size"])
        u_sz = int(self.prefs["ui_font_size"])

        accent_fg = best_contrast_fg(t["misora_pink"])
        panel_fg = best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff")
        editor_fg = best_contrast_fg(t["bg_editor"], t["fg_text"], "#ffffff")
        hl_fg = best_contrast_fg(t["highlight_bg"], t["fg_text"], "#ffffff")

        self.configure(bg=t["bg_dark"])

        for menu_obj in getattr(self, "_all_menus", []):
            try:
                menu_obj.configure(
                    bg=t["bg_panel"],
                    fg=panel_fg,
                    activebackground=t["misora_pink"],
                    activeforeground=accent_fg,
                )
            except Exception:
                pass

        def walk(w: tk.Widget) -> None:
            role = getattr(w, "_misora_role", None)
            try:
                if role == "dark":
                    w.configure(bg=t["bg_dark"])
                elif role == "panel":
                    w.configure(bg=t["bg_panel"])
                elif role == "ribbon":
                    w.configure(bg=t["bg_editor"], highlightbackground=t["border"])
                elif role == "panel_box":
                    w.configure(bg=t["bg_panel"], highlightbackground=t["border"])
                elif role == "editor_box":
                    w.configure(bg=t["bg_editor"])
                elif role == "sash":
                    w.configure(bg=t["border"])
                elif role == "label_panel":
                    w.configure(bg=t["bg_panel"], fg=panel_fg, font=("Segoe UI", u_sz))
                elif role == "label_muted":
                    w.configure(bg=t["bg_panel"], fg=t["fg_muted"], font=("Segoe UI", max(8, u_sz - 1)))
                elif role == "label_ribbon":
                    w.configure(bg=t["bg_editor"], fg=t["fg_muted"], font=("Segoe UI", max(8, u_sz - 1), "bold"))
                elif role == "label_accent":
                    w.configure(bg=t["bg_panel"], fg=t["misora_pink"], font=("Segoe UI", u_sz, "bold"))
                elif role == "label_voice":
                    w.configure(bg=t["bg_panel"], fg=t["accent_blue"], font=("Segoe UI", max(8, u_sz - 1)))
                elif role == "label_sep":
                    w.configure(bg=t["bg_panel"], fg=t["border"])
                elif role == "label_ribbon_sep":
                    w.configure(bg=t["bg_editor"], fg=t["border"])
                elif role == "ribbon_primary_btn":
                    w.configure(
                        bg=t["misora_pink"],
                        fg=accent_fg,
                        activebackground=t["misora_pink_hover"],
                        activeforeground=accent_fg,
                    )
                elif role == "ribbon_btn":
                    dark_p = self._is_dark_color(t["bg_panel"])
                    r_btn_bg = self._shift_hex(t["bg_panel"], 10 if dark_p else -8)
                    r_btn_h = self._shift_hex(t["bg_panel"], 22 if dark_p else -16)
                    r_btn_fg = best_contrast_fg(r_btn_bg, t["fg_text"], "#ffffff")
                    w.configure(
                        bg=r_btn_bg,
                        fg=r_btn_fg,
                        activebackground=r_btn_h,
                        activeforeground=r_btn_fg,
                    )
                elif role in ("ribbon_undo_btn", "ribbon_redo_btn"):
                    dark_p = self._is_dark_color(t["bg_panel"])
                    r_btn_bg = self._shift_hex(t["bg_panel"], 10 if dark_p else -8)
                    r_btn_h = self._shift_hex(t["bg_panel"], 22 if dark_p else -16)
                    grn = t.get("accent_green", "#2e7d32")
                    w.configure(
                        bg=r_btn_bg,
                        fg=grn,
                        activebackground=r_btn_h,
                        activeforeground=grn,
                    )
                elif role == "check_panel":
                    w.configure(
                        bg=t["bg_panel"],
                        fg=panel_fg,
                        selectcolor=t["bg_dark"],
                        activebackground=t["bg_panel"],
                        activeforeground=panel_fg,
                        font=("Segoe UI", u_sz),
                    )
                elif role == "check_accent":
                    w.configure(
                        bg=t["bg_panel"],
                        fg=panel_fg,
                        selectcolor=t["bg_dark"],
                        activebackground=t["bg_panel"],
                        activeforeground=t["misora_pink"],
                        font=("Segoe UI", max(8, u_sz - 1), "bold"),
                    )
                elif role == "check_ribbon":
                    w.configure(
                        bg=t["bg_editor"],
                        fg=editor_fg,
                        selectcolor=t["bg_panel"],
                        activebackground=t["bg_editor"],
                        activeforeground=t["misora_pink"],
                        font=("Segoe UI", max(8, u_sz - 1), "bold"),
                    )
                elif role == "entry_editor":
                    w.configure(
                        bg=t["bg_editor"],
                        fg=editor_fg,
                        insertbackground=t["misora_pink"],
                        highlightbackground=t["border"],
                        highlightcolor=t["misora_pink"],
                    )
                elif role == "entry_speaker":
                    w.configure(
                        bg=t["bg_editor"],
                        fg=editor_fg,
                        insertbackground=t["misora_pink"],
                        selectbackground=t["highlight_bg"],
                        selectforeground=hl_fg,
                        font=(d_fam, max(9, d_sz - 1), "bold"),
                    )
            except Exception:
                pass

            for child in w.winfo_children():
                walk(child)

        walk(self)
        # Also re-theme any currently-open child Toplevel windows
        for child_win in self.winfo_children():
            if isinstance(child_win, tk.Toplevel) and child_win.winfo_exists():
                try:
                    child_win.configure(bg=t["bg_panel"])
                except Exception:
                    pass
                walk(child_win)

        self.txt_results.configure(
            bg=t["bg_editor"],
            fg=editor_fg,
            font=("Segoe UI", u_sz),
        )
        self.txt_results.tag_configure("file_header", font=("Segoe UI", u_sz, "bold"), foreground=t["misora_pink"])
        self.txt_results.tag_configure("box_badge", font=("Consolas", max(8, u_sz - 1), "bold"), foreground=t["accent_blue"])
        self.txt_results.tag_configure("speaker_tag", font=("Segoe UI", u_sz, "bold"), foreground=editor_fg)
        self.txt_results.tag_configure("selected_row", background=t["highlight_bg"], foreground=hl_fg)
        self.txt_results.tag_configure(
            "match_hl",
            background=t["misora_pink"],
            foreground=accent_fg,
            font=("Segoe UI", u_sz, "bold"),
        )

        if hasattr(self, "txt_opened_files"):
            self.txt_opened_files.configure(
                bg=t["bg_editor"],
                fg=editor_fg,
                font=("Segoe UI", u_sz),
            )
            self.txt_opened_files.tag_configure("file_active", font=("Segoe UI", u_sz, "bold"), foreground=t["misora_pink"], background=t["highlight_bg"])
            self.txt_opened_files.tag_configure("file_dirty", font=("Segoe UI", u_sz, "bold"), foreground=t["accent_yellow"])
            self.txt_opened_files.tag_configure("file_normal", font=("Segoe UI", u_sz), foreground=editor_fg)
            self.txt_opened_files.tag_configure("file_dim", font=("Segoe UI", max(8, u_sz - 1)), foreground=t["fg_muted"])

        gutter_bg = "#e8e8e8" if self._is_light_theme() else "#2d2d30"
        gutter_fg = "#707070" if self._is_light_theme() else "#858585"
        if hasattr(self, "gutter_clean"):
            self.gutter_clean.configure(bg=gutter_bg, fg=gutter_fg)
        if hasattr(self, "gutter_cont"):
            self.gutter_cont.configure(bg=gutter_bg, fg=gutter_fg)
        if hasattr(self, "ruler_clean"):
            self.ruler_clean.configure(bg=gutter_bg, fg=gutter_fg)
        if hasattr(self, "ruler_cont"):
            self.ruler_cont.configure(bg=gutter_bg, fg=gutter_fg)

        self.txt_dialogue.configure(
            font=(d_fam, d_sz),
            bg=t["bg_editor"],
            fg=editor_fg,
            insertbackground=t["misora_pink"],
            selectbackground=t["highlight_bg"],
            selectforeground=hl_fg,
            highlightthickness=0,
            bd=1,
            relief="solid",
        )
        self._configure_editor_rich_tags(self.txt_dialogue, d_fam, d_sz)

        self.txt_continuous.configure(
            font=(d_fam, d_sz),
            bg=t["bg_editor"],
            fg=editor_fg,
            insertbackground=t["misora_pink"],
            selectbackground=t["highlight_bg"],
            selectforeground=hl_fg,
            highlightthickness=0,
            bd=1,
            relief="solid",
        )
        if hasattr(self, "txt_box0_summary"):
            self.txt_box0_summary.configure(
                font=(d_fam, d_sz),
                bg=t["bg_editor"],
                fg=editor_fg,
                insertbackground=t["misora_pink"],
                selectbackground=t["highlight_bg"],
                selectforeground=hl_fg,
                highlightthickness=0,
                bd=1,
                relief="solid",
            )
            self._configure_editor_rich_tags(self.txt_box0_summary, d_fam, d_sz)
        if hasattr(self, "entry_box0_title"):
            self.entry_box0_title.configure(
                font=(d_fam, d_sz),
                bg=t["bg_editor"],
                fg=editor_fg,
                insertbackground=t["misora_pink"],
            )
        if hasattr(self, "entry_box0_subtitle"):
            self.entry_box0_subtitle.configure(
                font=(d_fam, d_sz),
                bg=t["bg_editor"],
                fg=editor_fg,
                insertbackground=t["misora_pink"],
            )

        if hasattr(self, "txt_raw"):
            self.txt_raw.configure(
                highlightthickness=0,
                bd=1,
                relief="solid",
            )
        self.txt_continuous.tag_configure("cont_divider", foreground=t["misora_pink"], font=("Consolas", max(8, d_sz - 1), "bold"), spacing1=4, spacing3=2)
        self.txt_continuous.tag_configure("cont_badge", foreground=t["misora_pink"], font=("Consolas", max(8, d_sz - 2), "bold"))
        self.txt_continuous.tag_configure("cont_speaker", foreground=editor_fg, font=(d_fam, max(9, d_sz - 1), "bold"))
        self.txt_continuous.tag_configure("cont_narrator", foreground=t["fg_muted"], font=(d_fam, max(8, d_sz - 2), "italic"))
        self.txt_continuous.tag_configure("cont_voice", foreground=t["accent_blue"], font=("Segoe UI", max(8, d_sz - 3)))
        self.txt_continuous.tag_configure("cont_active_header", background=t["highlight_bg"])
        self.txt_continuous.tag_configure("cont_body", foreground=editor_fg, font=(d_fam, d_sz))
        self._configure_editor_rich_tags(self.txt_continuous, d_fam, d_sz)

        raw_bg = self._shift_hex(t["bg_editor"], -6)
        self.txt_raw.configure(
            font=("Consolas", r_sz),
            bg=raw_bg,
            fg=t["fg_muted"],
            insertbackground=t["misora_pink"],
        )

        if hasattr(self, "txt_console"):
            self._apply_console_theme()

        if hasattr(self, "txt_glossary"):
            self.txt_glossary.configure(bg=t["bg_editor"], fg=editor_fg, font=("Segoe UI", u_sz))
            self.txt_glossary.tag_configure("gl_tag", font=("Consolas", u_sz, "bold"), foreground=t["misora_pink"])
            self.txt_glossary.tag_configure("gl_title", font=("Segoe UI", u_sz, "bold"), foreground=editor_fg)
            self.txt_glossary.tag_configure("gl_syntax", font=("Consolas", max(8, u_sz - 1)), foreground=t["accent_blue"])
            self.txt_glossary.tag_configure("gl_desc", font=("Segoe UI", max(8, u_sz - 1)), foreground=t["fg_muted"])
            self.txt_glossary.tag_configure("gl_selected", background=t["highlight_bg"], foreground=hl_fg)
            self._render_glossary_list()

        for key, btn in self._theme_swatch_buttons.items():
            if key in t:
                btn.configure(bg=t[key], activebackground=t[key])
            if key in self._theme_hex_vars and self._theme_hex_vars[key].get().lower() != t[key].lower():
                self._theme_hex_vars[key].set(t[key])

        if self.var_preview_compiled.get():
            self._update_views()
        else:
            self._highlight_ngui_tags()
            self._auto_resize_dialogue_box()

        if save:
            self._save_user_prefs()

    def set_status(
        self,
        message: str,
        is_error: bool = False,
        timeout_ms: Optional[int] = None,
    ) -> None:
        """Update the main status bar label text with contrast/error styling and optional timeout."""
        try:
            if hasattr(self, "_status_after_id") and self._status_after_id:
                try:
                    self.after_cancel(self._status_after_id)
                except Exception:
                    pass
                self._status_after_id = None

            if not hasattr(self, "lbl_status") or not self.lbl_status or not self.lbl_status.winfo_exists():
                return

            t = self.theme
            if is_error:
                error_fg = "#d94862" if t.get("fg_muted") != "#d94862" else "#ff7da7"
                self.lbl_status.config(text=message, fg=error_fg)
            else:
                normal_fg = t.get("fg_muted", "#9c8ec0")
                self.lbl_status.config(text=message, fg=normal_fg)

            if timeout_ms is not None and timeout_ms > 0:
                self._status_after_id = self.after(timeout_ms, self._reset_status)
        except Exception:
            pass

    def _reset_status(self) -> None:
        """Restore the status bar to default text and normal theme styling."""
        try:
            self._status_after_id = None
            if hasattr(self, "lbl_status") and self.lbl_status and self.lbl_status.winfo_exists():
                t = self.theme
                self.lbl_status.config(
                    text=self._default_status_text,
                    fg=t.get("fg_muted", "#9c8ec0"),
                )
        except Exception:
            pass

    def show_toast(
        self,
        message: str,
        duration_ms: int = 2200,
        is_accent: bool = True,
        is_error: bool = False,
        status_bar: bool = True,
    ) -> None:
        """Display a non-intrusive floating toast notification above the action bar."""
        try:
            if status_bar:
                self.set_status(message, is_error=is_error)

            # Check if active toast has identical message (coalesce duplicate)
            if self._toast_active and hasattr(self, "_toast_widget") and self._toast_widget and self._toast_widget.winfo_exists():
                try:
                    current_text = self._toast_widget.cget("text")
                except Exception:
                    current_text = None
                if current_text == message:
                    if self._toast_after_id:
                        try:
                            self.after_cancel(self._toast_after_id)
                        except Exception:
                            pass
                    self._toast_after_id = self.after(duration_ms, self._dismiss_toast)
                    return

            if self._toast_active:
                if hasattr(self, "_toast_queue"):
                    if self._toast_queue and self._toast_queue[-1][0] == message:
                        return
                    self._toast_queue.append((message, duration_ms, is_accent, is_error))
                return

            self._display_toast(message, duration_ms, is_accent, is_error)
        except Exception:
            pass

    def _display_toast(
        self,
        message: str,
        duration_ms: int,
        is_accent: bool,
        is_error: bool,
    ) -> None:
        """Render and place the toast widget with appropriate theme styling and auto-dismiss timer."""
        try:
            self._toast_active = True
            if not hasattr(self, "_toast_widget") or not self._toast_widget or not self._toast_widget.winfo_exists():
                self._toast_widget = tk.Label(
                    self,
                    text="",
                    font=("Segoe UI", 10, "bold"),
                    bd=1,
                    relief="solid",
                    padx=14,
                    pady=6,
                    cursor="hand2",
                )
                self._toast_widget.bind("<Button-1>", lambda _e=None: self._dismiss_toast())

            t = self.theme
            if is_error:
                bg_col = "#d94862"
                fg_col = best_contrast_fg(bg_col, "#14141a", "#ffffff")
            elif is_accent:
                bg_col = t.get("misora_pink", "#a66cff")
                fg_col = best_contrast_fg(bg_col)
            else:
                bg_col = t.get("bg_editor", "#282c34")
                fg_col = best_contrast_fg(bg_col)

            border_col = t.get("border", "#4b5263")
            self._toast_widget.configure(
                text=message,
                bg=bg_col,
                fg=fg_col,
                highlightthickness=1,
                highlightbackground=border_col,
            )
            # Geometry: place anchored south-east above action bar without occluding buttons
            self._toast_widget.place(relx=1.0, rely=1.0, x=-16, y=-52, anchor="se")
            self._toast_widget.lift()

            if hasattr(self, "_toast_after_id") and self._toast_after_id:
                try:
                    self.after_cancel(self._toast_after_id)
                except Exception:
                    pass
                self._toast_after_id = None

            self._toast_after_id = self.after(duration_ms, self._dismiss_toast)
        except Exception:
            self._toast_active = False

    def _dismiss_toast(self) -> None:
        """Dismiss active toast and display next queued notification if any."""
        try:
            if hasattr(self, "_toast_after_id") and self._toast_after_id:
                try:
                    self.after_cancel(self._toast_after_id)
                except Exception:
                    pass
                self._toast_after_id = None

            if hasattr(self, "_toast_widget") and self._toast_widget and self._toast_widget.winfo_exists():
                self._toast_widget.place_forget()

            if hasattr(self, "_toast_queue") and self._toast_queue:
                msg, dur, acc, err = self._toast_queue.popleft()
                if len(self._toast_queue) > 2 and dur > 1200:
                    dur = 1200
                self._display_toast(msg, dur, acc, err)
            else:
                self._toast_active = False
        except Exception:
            self._toast_active = False

    def _configure_editor_rich_tags(self, widget: tk.Text, d_fam: str, d_sz: int) -> None:
        """Configure syntax highlight & compiled NGUI preview tags on a dialogue text widget."""
        t = self.theme
        hl_fg = best_contrast_fg(t["highlight_bg"], t["misora_pink"], "#ffffff")
        widget.tag_configure(
            "secret_whitespace",
            background="",
        )
        widget.tag_configure(
            "ngui_tag",
            foreground=t["accent_yellow"],
            font=("Consolas", max(8, d_sz - 1)),
        )
        widget.tag_configure(
            "compiled_ruby",
            foreground=hl_fg,
            background=t["highlight_bg"],
            font=(d_fam, max(7, d_sz - 3), "bold"),
            offset=5,
        )
        widget.tag_configure(
            "compiled_player",
            foreground=best_contrast_fg(t["highlight_bg"], t["accent_blue"], "#ffffff"),
            background=t["highlight_bg"],
            font=(d_fam, d_sz, "bold"),
        )
        widget.tag_configure(
            "search_hit",
            background=t["highlight_bg"],
            foreground=hl_fg,
            underline=True,
        )
        for tag_name in list(widget.tag_names()):
            if tag_name.startswith("cstyle_"):
                widget.tag_delete(tag_name)
        widget.tag_raise("ngui_tag")
        widget.tag_raise("search_hit")

    # -------------------------------------------------------------------------
    # Native Windows Drag & Drop — Crash-Safe Single-HWND Subclassing (#1)
    # -------------------------------------------------------------------------
    def _init_drag_and_drop(self) -> None:
        """Register native Win32 WM_DROPFILES handler safely on the top-level outer HWND."""
        if sys.platform != "win32":
            return

        try:
            self.update_idletasks()
            user32 = ctypes.windll.user32
            shell32 = ctypes.windll.shell32

            is_64bit = ctypes.sizeof(ctypes.c_void_p) == 8
            GWLP_WNDPROC = -4
            WM_DROPFILES = 0x0233
            WM_COPYDATA = 0x004A
            WM_COPYGLOBALDATA = 0x0049
            MSGFLT_ALLOW = 1

            LRESULT = ctypes.c_ssize_t
            LONG_PTR = ctypes.c_ssize_t

            user32.GetParent.argtypes = [wintypes.HWND]
            user32.GetParent.restype = wintypes.HWND

            shell32.DragAcceptFiles.argtypes = [wintypes.HWND, wintypes.BOOL]
            shell32.DragAcceptFiles.restype = None

            shell32.DragQueryFileW.argtypes = [
                wintypes.HANDLE, wintypes.UINT, wintypes.LPWSTR, wintypes.UINT
            ]
            shell32.DragQueryFileW.restype = wintypes.UINT

            shell32.DragFinish.argtypes = [wintypes.HANDLE]
            shell32.DragFinish.restype = None

            user32.CallWindowProcW.argtypes = [
                LONG_PTR, wintypes.HWND, wintypes.UINT,
                wintypes.WPARAM, wintypes.LPARAM
            ]
            user32.CallWindowProcW.restype = LRESULT

            get_wnd_proc = user32.GetWindowLongPtrW if is_64bit else user32.GetWindowLongW
            get_wnd_proc.argtypes = [wintypes.HWND, ctypes.c_int]
            get_wnd_proc.restype = LONG_PTR

            set_wnd_proc = user32.SetWindowLongPtrW if is_64bit else user32.SetWindowLongW
            set_wnd_proc.argtypes = [wintypes.HWND, ctypes.c_int, LONG_PTR]
            set_wnd_proc.restype = LONG_PTR

            inner_hwnd = int(self.winfo_id())
            parent_hwnd = int(user32.GetParent(inner_hwnd) or 0)
            target_hwnd = parent_hwnd if parent_hwnd else inner_hwnd
            self._drop_hwnd = target_hwnd

            try:
                user32.ChangeWindowMessageFilterEx.argtypes = [
                    wintypes.HWND, wintypes.UINT, wintypes.DWORD, ctypes.c_void_p
                ]
                user32.ChangeWindowMessageFilterEx.restype = wintypes.BOOL
                for hwnd in {h for h in (target_hwnd, inner_hwnd) if h}:
                    for msg_id in (WM_DROPFILES, WM_COPYDATA, WM_COPYGLOBALDATA):
                        user32.ChangeWindowMessageFilterEx(hwnd, msg_id, MSGFLT_ALLOW, None)
            except Exception as filter_exc:
                self.logger.debug("Drag & Drop", f"ChangeWindowMessageFilterEx skipped: {filter_exc}")

            WNDPROC = ctypes.WINFUNCTYPE(
                LRESULT, wintypes.HWND, wintypes.UINT,
                wintypes.WPARAM, wintypes.LPARAM
            )

            self._wndprocs = {}

            def _make_wndproc(orig_proc_addr: int):
                def _wndproc(hwnd, msg, wparam, lparam):
                    try:
                        if msg == WM_DROPFILES:
                            hdrop = wintypes.HANDLE(wparam)
                            dropped: List[Path] = []
                            try:
                                count = shell32.DragQueryFileW(hdrop, 0xFFFFFFFF, None, 0)
                                for idx in range(count):
                                    length = shell32.DragQueryFileW(hdrop, idx, None, 0)
                                    if length > 0:
                                        buf = ctypes.create_unicode_buffer(length + 1)
                                        shell32.DragQueryFileW(hdrop, idx, buf, length + 1)
                                        if buf.value:
                                            dropped.append(Path(buf.value))
                            finally:
                                shell32.DragFinish(hdrop)

                            if dropped and not self._dnd_in_progress:
                                self._dnd_in_progress = True
                                self.after(50, self._handle_dropped_paths, dropped)
                            return 0
                    except Exception as cb_exc:
                        self.logger.exception("Drag & Drop WNDPROC error:", cb_exc)
                        return 0

                    return user32.CallWindowProcW(orig_proc_addr, hwnd, msg, wparam, lparam)

                return WNDPROC(_wndproc)

            shell32.DragAcceptFiles(target_hwnd, True)
            orig_addr = int(get_wnd_proc(target_hwnd, GWLP_WNDPROC) or 0)
            if orig_addr:
                cb = _make_wndproc(orig_addr)
                cb_addr = ctypes.cast(cb, ctypes.c_void_p).value
                set_wnd_proc(target_hwnd, GWLP_WNDPROC, cb_addr)
                self._wndprocs[target_hwnd] = (cb, orig_addr)
                self.logger.debug("Drag & Drop", f"Subclassed top-level HWND={hex(target_hwnd)}")
        except Exception as e:
            self.logger.warning("Drag & Drop", f"Drag-and-drop hook warning: {e}")

    def _cleanup_drag_and_drop(self) -> None:
        """Restore original WNDPROC on registered HWNDs prior to window destruction."""
        if sys.platform != "win32" or not self._wndprocs:
            return
        try:
            user32 = ctypes.windll.user32
            is_64bit = ctypes.sizeof(ctypes.c_void_p) == 8
            GWLP_WNDPROC = -4
            LONG_PTR = ctypes.c_ssize_t
            set_wnd_proc = user32.SetWindowLongPtrW if is_64bit else user32.SetWindowLongW
            set_wnd_proc.argtypes = [wintypes.HWND, ctypes.c_int, LONG_PTR]
            set_wnd_proc.restype = LONG_PTR

            for hwnd, (_cb, orig_addr) in list(self._wndprocs.items()):
                try:
                    if user32.IsWindow(hwnd) and orig_addr:
                        set_wnd_proc(hwnd, GWLP_WNDPROC, orig_addr)
                except Exception:
                    pass
            self._wndprocs.clear()
        except Exception:
            pass

    def on_force_open_file(self) -> None:
        """Prompt user to open ANY file (bypassing format/extension guards) as raw/plain text."""
        p = filedialog.askopenfilename(
            title="Force Open Any File (Raw / Plain Text)",
            filetypes=[("All Files (*.*)", "*.*")],
            initialdir=str(self.last_opened_dir) if getattr(self, "last_opened_dir", None) else None,
        )
        if p:
            self.open_file(Path(p))

    def _check_batch_safety(self, files: List[Path]) -> bool:
        """Prompt confirmation if dropping many files or very large files."""
        batch_thresh = getattr(self, "dnd_batch_threshold", 10)
        size_thresh_mb = getattr(self, "dnd_size_threshold_mb", 25.0)

        # 1. Batch count check
        if batch_thresh > 0 and len(files) > batch_thresh:
            ok = messagebox.askyesno(
                "Confirm Large Batch",
                f"You are about to open {len(files)} files at once.\n\n"
                f"Opening many files may take a few moments. Proceed?",
                default=messagebox.YES,
            )
            if not ok:
                return False

        # 2. File size check
        if size_thresh_mb > 0:
            large_files: List[Tuple[Path, float]] = []
            for f in files:
                try:
                    sz_mb = f.stat().st_size / (1024 * 1024)
                    if sz_mb >= size_thresh_mb:
                        large_files.append((f, sz_mb))
                except Exception:
                    pass
            if large_files:
                sample_list = "\n".join(f"• {f.name} ({sz:.1f} MB)" for f, sz in large_files[:5])
                if len(large_files) > 5:
                    sample_list += f"\n• ... and {len(large_files) - 5} more"
                ok = messagebox.askyesno(
                    "Confirm Large File(s)",
                    f"The following file(s) exceed {size_thresh_mb:g} MB:\n\n"
                    f"{sample_list}\n\n"
                    f"Opening very large files may consume extra memory. Proceed?",
                    default=messagebox.YES,
                )
                if not ok:
                    return False
        return True

    def _on_dnd_settings_dialog(self) -> None:
        """Dialog to configure Drag & Drop safety thresholds and filters."""
        t = self.theme
        dlg = tk.Toplevel(self)
        dlg.title("Drag & Drop Safety Settings")
        dlg.geometry("480x280")
        dlg.minsize(440, 240)
        dlg.transient(self)
        dlg.grab_set()
        dlg.configure(bg=t["bg_panel"])

        fg_panel = best_contrast_fg(t["bg_panel"])
        fg_editor = best_contrast_fg(t["bg_editor"])

        content = tk.Frame(dlg, bg=t["bg_panel"], padx=18, pady=16)
        content.pack(fill="both", expand=True)

        tk.Label(
            content,
            text="Drag & Drop Safety Settings",
            font=("Segoe UI", 11, "bold"),
            bg=t["bg_panel"],
            fg=t["misora_pink"],
        ).pack(anchor="w", pady=(0, 10))

        var_filter = tk.BooleanVar(master=dlg, value=getattr(self, "dnd_filter_binary", True))
        cb = tk.Checkbutton(
            content,
            text="Filter out binary files (.exe, .dll, images, media, archives) on drop",
            variable=var_filter,
            font=("Segoe UI", 9),
            bg=t["bg_panel"],
            fg=fg_panel,
            selectcolor=t["bg_dark"],
        )
        cb.pack(anchor="w", pady=(0, 10))

        # Row 1: Batch threshold
        r1 = tk.Frame(content, bg=t["bg_panel"])
        r1.pack(fill="x", pady=4)
        tk.Label(r1, text="Batch prompt threshold (files):", font=("Segoe UI", 9), bg=t["bg_panel"], fg=fg_panel, width=28, anchor="w").pack(side="left")
        var_batch = tk.StringVar(master=dlg, value=str(getattr(self, "dnd_batch_threshold", 10)))
        ent_batch = tk.Entry(r1, textvariable=var_batch, width=8, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid")
        ent_batch.pack(side="left", padx=4)
        tk.Label(r1, text="(0 = never prompt)", font=("Segoe UI", 8), bg=t["bg_panel"], fg=t["fg_muted"]).pack(side="left", padx=4)

        # Row 2: Size threshold
        r2 = tk.Frame(content, bg=t["bg_panel"])
        r2.pack(fill="x", pady=4)
        tk.Label(r2, text="Large file threshold (MB):", font=("Segoe UI", 9), bg=t["bg_panel"], fg=fg_panel, width=28, anchor="w").pack(side="left")
        var_size = tk.StringVar(master=dlg, value=str(getattr(self, "dnd_size_threshold_mb", 25.0)))
        ent_size = tk.Entry(r2, textvariable=var_size, width=8, font=("Segoe UI", 9), bg=t["bg_editor"], fg=fg_editor, bd=1, relief="solid")
        ent_size.pack(side="left", padx=4)
        tk.Label(r2, text="(0 = never prompt)", font=("Segoe UI", 8), bg=t["bg_panel"], fg=t["fg_muted"]).pack(side="left", padx=4)

        # Bottom buttons
        btn_bar = tk.Frame(dlg, bg=t["bg_panel"], padx=18, pady=12)
        btn_bar.pack(fill="x", side="bottom")

        def _safe_close(_e: Optional[tk.Event] = None):
            safe_grab_release(dlg)
            dlg.destroy()

        def _save():
            try:
                b_val = max(0, int(var_batch.get().strip()))
            except ValueError:
                b_val = 10
            try:
                s_val = max(0.0, float(var_size.get().strip()))
            except ValueError:
                s_val = 25.0
            self.dnd_batch_threshold = b_val
            self.dnd_size_threshold_mb = s_val
            self.dnd_filter_binary = bool(var_filter.get())
            self._save_user_prefs(silent=True)
            self.lbl_status.config(text="Drag & Drop safety settings saved.")
            safe_grab_release(dlg)
            dlg.destroy()
            messagebox.showinfo(
                "Settings Saved",
                "Drag & Drop safety settings have been saved.",
                parent=self,
            )

        dlg.protocol("WM_DELETE_WINDOW", _safe_close)
        dlg.bind("<Escape>", _safe_close)
        ttk.Button(btn_bar, text="Save Settings", style="Accent.TButton", command=_save).pack(side="left", padx=(0, 6))
        ttk.Button(btn_bar, text="Cancel", style="TButton", command=_safe_close).pack(side="left")

    def _handle_dropped_paths(self, paths: List[Path]) -> None:
        """Process files or folders dropped onto the Misora window safely."""
        self._dnd_in_progress = False  # reset early so crashes don't lock DnD
        try:
            if not paths:
                return
            self.logger.info("Drag & Drop", f"Received {len(paths)} dropped item(s): {[str(p) for p in paths]}")

            known_binary_exts = {
                ".exe", ".dll", ".so", ".dylib", ".bin", ".dat",
                ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico", ".tga",
                ".zip", ".7z", ".rar", ".tar", ".gz", ".bz2",
                ".db", ".sqlite", ".db3",
                ".mp3", ".wav", ".ogg", ".flac", ".aac",
                ".mp4", ".mkv", ".avi", ".mov", ".usm",
                ".pdf", ".doc", ".docx", ".xls", ".xlsx"
            }

            files = [p for p in paths if p.is_file()]
            dirs = [p for p in paths if p.is_dir()]

            # Guard: check for completely empty files (0 bytes)
            if files:
                empty_files = [f for f in files if f.stat().st_size == 0]
                if empty_files and len(empty_files) == len(files):
                    self.lbl_status.config(text="Dropped file(s) are empty (0 bytes). Scope and documents unchanged.")
                    messagebox.showwarning(
                        "Empty File(s)",
                        f"The dropped file(s) are completely empty (0 bytes).\n\n"
                        f"No files were opened, and search/project scopes were left unchanged.",
                        parent=self
                    )
                    return

            # 1. Process dropped files
            if files:
                filter_bin = getattr(self, "dnd_filter_binary", True)
                if filter_bin:
                    to_open = [f for f in files if f.suffix.lower() not in known_binary_exts and f.stat().st_size > 0]
                    skipped = [f for f in files if f.suffix.lower() in known_binary_exts or f.stat().st_size == 0]
                else:
                    to_open = [f for f in files if f.stat().st_size > 0]
                    skipped = [f for f in files if f.stat().st_size == 0]

                if skipped and not to_open:
                    self.lbl_status.config(
                        text=f"Skipped {len(skipped)} binary/unsupported file(s). Use 'File -> Force Open Any File...' to override."
                    )
                    self.logger.warning("Drag & Drop", f"Skipped binary/empty files: {[f.name for f in skipped]}")
                elif to_open:
                    if self._check_batch_safety(to_open):
                        opened = 0
                        for f in to_open:
                            try:
                                self.open_file(f)
                                opened += 1
                            except Exception as exc:  # noqa: BLE001
                                self.logger.error("Drag & Drop", f"Could not open {f.name}: {exc}")
                        msg = f"Opened {opened} file(s) via drag & drop."
                        if skipped:
                            msg += f" ({len(skipped)} binary file(s) skipped)"
                        self.lbl_status.config(text=msg)
                    else:
                        self.lbl_status.config(text="File drop cancelled by user.")

            # 2. Process dropped folder(s)
            if dirs:
                if len(dirs) > 1:
                    extra_count = len(dirs) - 1
                    extra_names = ", ".join(f"'{d.name}'" for d in dirs[1:4])
                    if extra_count > 3:
                        extra_names += f" and {extra_count - 3} more"
                    warn_msg = f"Multiple folders dropped ({len(dirs)}). Opened first folder '{dirs[0].name}'; remaining {extra_count} folder(s) ignored."
                    self.lbl_status.config(text=warn_msg)
                    self.show_toast(f"⚠ Only 1 folder opened. {extra_count} ignored: {extra_names}")
                    self.logger.warning("Drag & Drop", warn_msg)
                self._process_opened_folder(dirs[0], source_label="Drag & Drop")
        except Exception as exc:
            self.logger.exception("Error while handling dropped path(s):", exc)
            messagebox.showerror("Drag & Drop Error", f"Failed to open dropped item:\n{exc}")
        finally:
            self._dnd_in_progress = False

    def _process_opened_folder(self, folder: Path, source_label: str = "Folder") -> None:
        """Handle opening a folder with consistent multi-file prompt, batch safety, and scope assignment."""
        folder = Path(folder).resolve()
        try:
            story_files = (
                sorted(folder.glob("*.unity3d")) +
                sorted(folder.glob("*.asset")) +
                sorted(folder.glob("*.txt"))
            )
        except (OSError, PermissionError) as scan_err:
            self.logger.error(source_label, f"Error scanning folder '{folder}': {scan_err}")
            messagebox.showerror("Folder Access Error", f"Could not access folder '{folder.name}':\n{scan_err}", parent=self)
            return

        if not story_files:
            if source_label == "Drag & Drop":
                self.lbl_status.config(
                    text=f"Dropped folder '{folder.name}' contains no story files (.unity3d/.asset/.txt). Scope unchanged."
                )
                self.show_toast(f"No story files in: {folder.name}")
                messagebox.showwarning(
                    "No Story Files Found",
                    f"Folder '{folder.name}' contains no Princess Connect story files (.unity3d, .asset, .txt).\n\n"
                    f"Search and project scopes were left completely unchanged.",
                    parent=self
                )
                return

            ans = True
            if source_label not in ("Test", "unittest"):
                ans = messagebox.askyesno(
                    "Set Search Scope",
                    f"No story files (.unity3d, .asset, .txt) were found in '{folder.name}'.\n\n"
                    f"Do you want to set your search scope to this folder anyway?",
                    parent=self,
                    default=messagebox.NO
                )
            if ans:
                self.selected_search_folder = folder
                self.last_opened_dir = folder
                self.folder_path_var.set(str(folder))
                self.scope_var.set("folder")
                self._sync_scope_widgets()
                self._save_user_prefs(silent=True)
                self.lbl_status.config(text=f"Search scope set to folder: '{folder.name}' (no story files found to open)")
                self.show_toast(f"Search folder set to: {folder.name}")
            return

        self.last_opened_dir = folder
        if len(story_files) == 1:
            try:
                self.open_file(story_files[0])
                self.scope_var.set("current")
                self._sync_scope_widgets()
                self._save_user_prefs(silent=True)
                self.lbl_status.config(
                    text=f"Opened \"{story_files[0].name}\" from folder. Search scope set to Current File(s)."
                )
            except Exception as exc:  # noqa: BLE001
                self.logger.error(source_label, f"Could not open {story_files[0].name}: {exc}")
        else:
            ans = messagebox.askyesnocancel(
                "Open Folder Story Files",
                f"Found {len(story_files)} story file(s) in folder '{folder.name}'.\n\n"
                f"  Yes    – Open all {len(story_files)} files as editor tabs\n"
                f"  No     – Set search scope to this folder only (open nothing)\n"
                f"  Cancel – Abort: do nothing, keep current state",
                default=messagebox.YES,
            )
            if ans is True:
                if self._check_batch_safety(story_files):
                    opened = 0
                    for sf in story_files:
                        try:
                            self.open_file(sf)
                            opened += 1
                        except Exception as exc:  # noqa: BLE001
                            self.logger.error(source_label, f"Could not open {sf.name}: {exc}")
                    # When all files are opened into tabs, switch scope to Current File(s)
                    self.scope_var.set("current")
                    self._sync_scope_widgets()
                    self._save_user_prefs(silent=True)
                    self.lbl_status.config(
                        text=f"Opened {opened} file(s) into tabs. Search scope set to Current File(s)."
                    )
                else:
                    self.lbl_status.config(text=f"{source_label} cancelled by user.")
            elif ans is False:
                # "No" = Set search scope to this folder only (open nothing)
                self.selected_search_folder = folder
                self.folder_path_var.set(str(folder))
                self.scope_var.set("folder")
                self._sync_scope_widgets()
                self._save_user_prefs(silent=True)
                self.lbl_status.config(
                    text=f"Search scope set to folder: '{folder.name}' ({len(story_files)} story file(s) found). No files opened."
                )
                self.show_toast(f"Search folder set to: {folder.name}")
            else:
                # "Cancel" = Abort: do nothing, touch nothing!
                self.lbl_status.config(text=f"{source_label} cancelled. No changes made.")

    # -------------------------------------------------------------------------
    # Environment & WCAG Contrast-Safe ttk Styling (#13, #4, #7)
    # -------------------------------------------------------------------------
    def _set_project_folder(self, folder: Union[str, Path]) -> None:
        """Central setter for project_folder; replaces XUAT search roots cleanly (Rule 1)."""
        p = Path(folder)
        self.project_folder = p
        self.bepinex_project_folder = p
        xuat_dir = self._resolve_xuat_text_root(p)
        self.xuat_search_roots = [xuat_dir] if (xuat_dir and xuat_dir.exists()) else []

    def _resolve_xuat_text_root(self, proj_dir: Optional[Path]) -> Optional[Path]:
        """Resolve XUAT text root strictly to BepInEx\\Translation\\en\\Text (or Text)."""
        if not proj_dir:
            return None
        candidates = [
            proj_dir / "BepInEx" / "Translation" / "en" / "Text",
            proj_dir / "Translation" / "en" / "Text",
            proj_dir / "Text",
        ]
        for c in candidates:
            if c.is_dir():
                return c
        return proj_dir if proj_dir.is_dir() else None

    def _resolve_project_search_roots(self, proj_dir: Optional[Path]) -> List[Path]:
        """
        Resolve Project Search cleanly into explicit bounded (Text, RedirectedResources) directories.
        Uses OR condition so if only Text exists, it returns [Text] without falling through to [proj_dir].
        CRITICAL INVARIANT: Strictly excludes BepInEx/plugins/ and BepInEx/config/.
        """
        if not proj_dir or not Path(proj_dir).exists():
            return []
        p = Path(proj_dir)

        # Check candidate locations for Text and RedirectedResources (OR condition per Guard 1)
        sub_bases = [
            p / "BepInEx" / "Translation" / "en",
            p / "Translation" / "en",
            p,
        ]
        for base in sub_bases:
            if base.is_dir():
                t_dir = base / "Text"
                r_dir = base / "RedirectedResources"
                roots = []
                if t_dir.is_dir():
                    roots.append(t_dir)
                if r_dir.is_dir():
                    roots.append(r_dir)
                if roots:
                    return roots

        # If base is itself Text or RedirectedResources
        if p.name.lower() in ("text", "redirectedresources") and p.is_dir():
            return [p]

        # Plain directory without BepInEx structure: return p, but never plugins or config
        if p.is_dir() and p.name.lower() not in ("plugins", "config"):
            return [p]
        return []

    def _detect_environment(self) -> None:
        """Auto-detect Priconne mod/translation project roots (BepInEx, MelonLoader, XUAT) and Notepad++."""
        candidates = [
            Path(r"C:\[Gacha]\PriconneRe-TL\src\BepInEx\Translation\en"),
            Path(r"C:\[Gacha]\PriconneRe-TL\src\BepInEx"),
        ]
        active_proj = getattr(self, "project_folder", None) or getattr(self, "bepinex_project_folder", None)
        if active_proj and active_proj.exists():
            candidates.insert(0, active_proj)

        found_proj = None
        for c in candidates:
            if c.exists():
                found_proj = c
                break

        # If user has not explicitly configured project_folder, adopt the detected mod root
        if not getattr(self, "project_folder", None) and found_proj:
            self._set_project_folder(found_proj)
        elif getattr(self, "project_folder", None):
            self._set_project_folder(self.project_folder)

        # Auto-detect Notepad++ if not already set
        if not self.notepadpp_path or not Path(self.notepadpp_path).exists():
            for npp_dir in (os.environ.get("ProgramFiles", r"C:\Program Files"), os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")):
                candidate = Path(npp_dir) / "Notepad++" / "notepad++.exe"
                if candidate.is_file():
                    self.notepadpp_path = candidate
                    break

    def _get_backup_dir(self) -> Path:
        """Return user-configured backup folder, defaulting to SCRIPT_DIR / 'backups'."""
        if self.backup_folder:
            p = Path(self.backup_folder)
            p.mkdir(parents=True, exist_ok=True)
            return p
        default_bak = SCRIPT_DIR / "backups"
        default_bak.mkdir(parents=True, exist_ok=True)
        return default_bak

