# misora.py PART 02/12 | ORIG L1424-L2898/17315 | SHA:ec4d9bfc8ec6
# SYMS: L1424:MisoraApp.__init__, L1723:MisoraApp.get_icon, L1727:MisoraApp.safe_clipboard_get, L1739:MisoraApp.safe_clipboard_set, L1755:MisoraApp._install_exception_hooks, L1764:MisoraApp.report_callback_exception, L1773:MisoraApp._on_app_exit, L1818:MisoraApp._on_root_destroy, L1873:MisoraApp.destroy, L1973:MisoraApp._load_user_prefs, L2097:MisoraApp._save_user_prefs, L2166:MisoraApp._detect_active_preset_name, L2173:MisoraApp._is_dark_color, L2178:MisoraApp._is_light_theme, L2182:MisoraApp._shift_hex, L2192:MisoraApp._tag_role, L2197:MisoraApp._apply_theme_and_fonts_live, L2490:MisoraApp.set_status, L2521:MisoraApp._reset_status, L2534:MisoraApp.show_toast, L2573:MisoraApp._display_toast, L2630:MisoraApp._dismiss_toast, L2653:MisoraApp._sweep_cstyle_tags, L2661:MisoraApp._configure_editor_rich_tags, L2713:MisoraApp._init_drag_and_drop, L2825:MisoraApp._cleanup_drag_and_drop, L2848:MisoraApp.on_force_open_file, L2858:MisoraApp._check_batch_safety

    def __init__(self, initial_path: Optional[str] = None, show_splash: bool = True, _progress_callback=None, restore_session: bool = True):
        super().__init__()
        self.title("Misora Editor: Unity3D Revision Tool & Story Editor")
        self.geometry("1280x820")
        self.minsize(980, 620)
        self.withdraw()   # stay hidden until splash closes or ready

        splash = None
        if show_splash and _progress_callback is None:
            try:
                splash = MisoraSplashScreen(parent=self)
                splash.process_events()
            except Exception:
                splash = None

        def _rpt(val: float, msg: str = ""):
            if splash:
                try:
                    splash.set_progress(val, msg)
                    splash.process_events()
                except Exception:
                    pass
            elif _progress_callback:
                try:
                    _progress_callback(val, msg)
                except Exception:
                    pass

        _rpt(0.10, "Loading core modules…")
        # Central Logger initialized early so startup & config load are recorded
        self.logger = MisoraLogger(DEBUG_LOG_PATH)
        self._install_exception_hooks()

        # Path config & persistent workspace states (initialized before _load_user_prefs)
        self.backup_folder: Optional[Path] = None
        self.project_folder: Optional[Path] = None
        self.bepinex_project_folder: Optional[Path] = None  # Backward-compatible alias
        self.datamine_exe: Optional[Path] = None
        self.external_editor_path: Optional[Path] = None
        self.notepadpp_path: Optional[Path] = None
        self._datamine_confirm_skip: bool = False
        self._left_dock_tab: str = "search"
        self._left_dock_width: int = 340
        self._dock_collapsed: bool = False
        self.show_line_numbers: bool = True
        self.show_column_ruler: bool = False
        self.mtl_config: MTLConfig = MTLConfig()
        self._translator_dialog: Optional[Any] = None
        self._side_drawer_pinned: bool = False
        self.dnd_batch_threshold: int = 10
        self.dnd_size_threshold_mb: float = 25.0
        self.dnd_filter_binary: bool = True

        _rpt(0.25, "Loading saved preferences…")
        # Load persistent user preferences (fonts, theme colors, paths, mtl settings)
        self.prefs: Dict[str, Any] = self._load_user_prefs()
        self.theme: Dict[str, str] = dict(self.prefs["theme"])
        THEME.update(self.theme)

        dbg_cfg = self.prefs.get("debug", {})
        self.logger.configure(
            level_name=dbg_cfg.get("level", "Info"),
            log_to_file=bool(dbg_cfg.get("log_to_file", False)),
            categories=dbg_cfg.get("categories"),
            log_file_path=DEBUG_LOG_PATH,
        )

        self.configure(bg=self.theme["bg_dark"])
        apply_window_icon(self)

        # State Variables
        self.current_file_path: Optional[Path] = None
        self.current_doc: Optional[StoryDocument] = None
        self.current_unity_env: Any = None
        self.current_text_obj: Any = None
        self.current_box_idx: int = 0
        self.is_box0_active: bool = False
        self.var_box0_title: tk.StringVar = tk.StringVar(master=self, value="")
        self.var_box0_subtitle: tk.StringVar = tk.StringVar(master=self, value="")
        self.is_bundle_file: bool = False
        self.is_dirty: bool = False
        self._plain_text_content: str = ""
        self.xuat_search_roots: List[Path] = []
        self.xuat_index: Optional[XuatIndex] = None
        self.xuat_entries: Optional[XuatIndex] = None
        self._xuat_index_queue: queue.Queue = queue.Queue()
        self._xuat_index_poll_id: Optional[str] = None
        self._xuat_index_seq: int = 0
        self._xuat_index_cancel: Optional[threading.Event] = None
        self._xuat_global_choice_overrides: Dict[str, str] = {}
        self._import_xuat_dialog: Optional[Any] = None
        self._ui_ready: bool = False
        self.selected_search_folder: Optional[Path] = None

        # Steps 3-4: Undo journal & opened-files cache
        self.undo_journal: MasterUndoJournal = MasterUndoJournal()
        self.open_documents: Dict[Path, Any] = {}   # path -> open doc info dict

        # Active NGUI Ribbon color state
        self._active_ngui_color: str = "#7b42bc"
        self._active_ngui_grad_end: str = "#ff7da7"
        self._color_picker_win: Optional[NguiColorPickerPopup] = None

        # Multi-box edit tracking for Continuous View & XUAT sync
        self._original_box_texts: Dict[int, str] = {}
        self._modified_boxes: Set[int] = set()
        # S2: Per-document saved-state checkpoint map (SHA-256 fingerprints keyed by resolved str(path))
        self._saved_state_checkpoints: Dict[str, str] = {}
        self._cont_header_spans: Dict[int, Tuple[str, str]] = {}
        self._suppress_continuous_events: bool = False
        self._card_widgets: Dict[int, Dict[str, Any]] = {}
        self.var_select_box_mode: tk.BooleanVar = tk.BooleanVar(master=self, value=False)
        self._selected_boxes: Set[int] = set()
        self._locked_boxes: Set[int] = set()
        self._locked_box_uids: Set[int] = set()
        self._modified_box_uids: Set[int] = set()
        self._original_jp_by_uid: Dict[int, str] = {}
        self._box_clipboard: List[Any] = []
        self._is_speaker_pinned: bool = False
        self._icon_cache: dict = {}
        self._cont_resize_job: Optional[str] = None

        # S8b-1: Toast & Status Notification Manager state
        self._toast_queue: collections.deque = collections.deque()
        self._toast_active: bool = False
        self._toast_after_id: Optional[str] = None
        self._status_after_id: Optional[str] = None
        self._default_status_text: str = "Ready. Drag & Drop or open a .unity3d bundle or folder to begin."
        self._toast_widget: Optional[tk.Label] = None

        # Side Drawer (Customization, NGUI Glossary, & MTL) state
        self._side_drawer_visible: bool = False
        self._side_drawer_tab: str = "customize"
        self._theme_swatch_buttons: Dict[str, tk.Button] = {}
        self._theme_hex_vars: Dict[str, tk.StringVar] = {}
        self._glossary_line_map: Dict[int, int] = {}
        self._selected_glossary_idx: int = 0
        self._filtered_glossary_items: List[Dict[str, str]] = list(NGUI_GLOSSARY_ITEMS)
        self._mtl_drawer_queue: queue.Queue = queue.Queue()
        self._mtl_drawer_poll_id: Optional[str] = None
        self._mtl_drawer_pending: int = 0
        self._mtl_drawer_req_seq: int = 0
        self._mtl_drawer_latest_seq: Dict[str, int] = {}
        self._mtl_drawer_cache: "collections.OrderedDict[Tuple[str, str], str]" = collections.OrderedDict()
        self._mtl_drawer_mode: str = "dialogue"
        self._mtl_drawer_cards: Dict[str, Dict[str, Any]] = {}
        self._mtl_drawer_engine_vars: Dict[str, tk.BooleanVar] = {}
        self._mtl_drawer_active_context: Optional[Tuple[str, int, Any, str]] = None
        self._mtl_all_req_seqs: Dict[Tuple[Any, str], int] = {}
        self._mtl_all_results: Dict[Tuple[str, int, Any, str], str] = {}
        self._mtl_all_statuses: Dict[Tuple[str, int, Any, str], str] = {}
        self._mtl_all_errors: Dict[Tuple[str, int, Any, str], str] = {}
        self._mtl_all_selected_uid: Any = None
        self._mtl_all_block_ranges: List[Tuple[int, int, Any]] = []
        self._mtl_all_last_ctx: Optional[Tuple[str, int, Any, str]] = None
        if not hasattr(self, "_mtl_drawer_enabled_engines") or not isinstance(self._mtl_drawer_enabled_engines, dict):
            self._mtl_drawer_enabled_engines: Dict[str, bool] = {
                "XUAT Cache": True,
                "Google": True,
                "DeepL": False,
                "Local / Sugoi": False,
                "LLM / OpenAI": False,
            }

        # Native Win32 Drag & Drop references (kept alive to prevent GC)
        self._wndprocs: Dict[int, Tuple[Any, Any]] = {}
        self._drop_hwnd: Any = None
        self._dnd_in_progress: bool = False

        # Debug Console state
        self._console_visible: bool = bool(dbg_cfg.get("console_visible", False))
        self.var_console_visible = tk.BooleanVar(master=self, value=self._console_visible)
        self.var_log_to_file = tk.BooleanVar(master=self, value=bool(dbg_cfg.get("log_to_file", False)))
        self.var_log_level = tk.StringVar(master=self, value=str(dbg_cfg.get("level", "Info")))
        self.var_console_autoscroll = tk.BooleanVar(master=self, value=True)
        self.var_log_categories: Dict[str, tk.BooleanVar] = {}
        saved_cats = dbg_cfg.get("categories", {}) if isinstance(dbg_cfg.get("categories"), dict) else {}
        for cat in LOG_CATEGORIES:
            enabled = True if cat == ALWAYS_ON_CATEGORY else bool(saved_cats.get(cat, True))
            self.var_log_categories[cat] = tk.BooleanVar(master=self, value=enabled)

        # Background search worker & highlighting state
        self.search_engine = ProjectSearchEngine()
        self.sync_manager = XUnitySyncManager()
        self.search_queue: queue.Queue = queue.Queue()
        self.search_cancel_flag: bool = False
        self.active_search_results: List[SearchResult] = []
        self.active_search_options: Optional[SearchOptions] = None
        self.search_file_groups: List[Dict[str, Any]] = []
        self._file_group_lookup: Dict[str, Dict[str, Any]] = {}
        self._result_line_map: Dict[int, Tuple[str, Any]] = {}
        self._result_idx_to_line: Dict[int, int] = {}
        self._selected_result_idx: Optional[int] = None

        # Background MTL worker queue and request sequencing (Rule 15 / BUG-27)
        self._mtl_queue: queue.Queue = queue.Queue()
        self._mtl_request_seq: int = 0
        self._latest_applied_mtl_seq: Dict[Any, int] = {}
        self._mtl_poll_job: Optional[str] = None
        self._hash_mtl_source = _hash_mtl_source
        self._get_box_uid = _get_box_uid

        # Auto-detect project paths
        self._detect_environment()

        _rpt(0.55, "Building UI layout…")
        # Build UI
        self._apply_styles()
        self._build_menu()
        self._build_search_bar()

        _rpt(0.70, "Initializing editor panels…")
        self._build_main_panels()
        self._build_side_drawer()
        self._build_status_bar()
        self._bind_shortcuts()

        _rpt(0.85, "Applying theme and fonts…")
        # Sync initial widget fonts & colors with saved preferences
        self._apply_theme_and_fonts_live(save=False)
        self._update_empty_state_visibility()

        # Flush config on exit and unhook Win32 WNDPROC cleanly
        self.protocol("WM_DELETE_WINDOW", self._on_app_exit)
        self.bind("<Destroy>", self._on_root_destroy)

        _rpt(0.85, "Enabling drag & drop…")
        # Enable native OS Drag & Drop safely on the outer frame HWND
        self._init_drag_and_drop()

        # Start periodic poll for background tasks
        self._search_poll_job = self.after(100, self._process_search_queue)
        self._mtl_poll_job = self.after(50, self._poll_mtl_queue)

        # Restore saved window geometry and view toggles (Bug #2 / S9c)
        if hasattr(self, "_saved_geometry") and self._saved_geometry:
            try:
                sw = self.winfo_screenwidth()
                sh = self.winfo_screenheight()
                safe_geom = sanitize_window_geometry(self._saved_geometry, sw, sh)
                self.geometry(safe_geom)
            except Exception:
                pass
        if hasattr(self, "_saved_continuous_view") and hasattr(self, "var_continuous_view"):
            if self._saved_continuous_view:
                self.var_continuous_view.set(True)
                self._on_toggle_continuous_view()
            else:
                self.var_continuous_view.set(False)
        if hasattr(self, "_saved_sync_xuat") and hasattr(self, "var_sync_xuat"):
            self.var_sync_xuat.set(self._saved_sync_xuat)

        _rpt(1.00, "Ready!")
        self.logger.info("UI / Theme / Config", f"Misora initialized. Config path: {CONFIG_PATH}")

        if splash:
            splash.close()

        # Reveal the main window instantly (DEP-9 / AGENTS.md §22)
        self.deiconify()

        self._rpt_done = True
        self._ui_ready = True
        # Defer session file restoration to idle loop so startup never hangs (BUG-35)
        def _deferred_restore() -> None:
            if not self.winfo_exists() or getattr(self, "_destroyed", False):
                return
            if restore_session and getattr(self, "xuat_search_roots", None) and self.xuat_index is None:
                self._refresh_xuat_index_async()
            if initial_path and os.path.exists(initial_path):
                init_p = Path(initial_path)
                if init_p.is_dir():
                    try:
                        self._process_opened_folder(init_p, source_label="Initial Path")
                    except Exception as exc:
                        self.logger.error("File I/O", f"Failed opening initial folder '{initial_path}': {exc}")
                else:
                    try:
                        self.open_file(init_p)
                    except Exception as exc:
                        self.logger.error("File I/O", f"Failed opening initial file '{initial_path}': {exc}")
            elif restore_session and hasattr(self, "_saved_opened_files") and self._saved_opened_files:
                for fp in self._saved_opened_files:
                    fp_exists = Path(fp).exists() if isinstance(fp, (str, Path)) else False
                    if fp_exists:
                        try:
                            self.open_file(fp)
                        except Exception as exc:
                            self.logger.error("File I/O", f"Failed restoring session file '{fp}': {exc}")
                if hasattr(self, "_saved_active_file") and self._saved_active_file:
                    act_exists = Path(self._saved_active_file).exists() if isinstance(self._saved_active_file, (str, Path)) else False
                    if act_exists:
                        try:
                            self.open_file(self._saved_active_file)
                        except Exception as exc:
                            self.logger.error("File I/O", f"Failed activating session file '{self._saved_active_file}': {exc}")

        self.after_idle(_deferred_restore)

    def get_icon(self, name: str, size: Tuple[int, int] = (18, 18)) -> Optional[tk.PhotoImage]:
        """Retrieve an illustrated icon PhotoImage bound to this MisoraApp Tk instance."""
        return get_icon(name, size, master=self)

    def safe_clipboard_get(self) -> str:
        """Read text from clipboard with retry on TclError and CRLF/CR normalization (AGENTS.md Rule 14)."""
        for _ in range(5):
            try:
                val = self.clipboard_get()
                return val.replace("\r\n", "\n").replace("\r", "\n")
            except tk.TclError:
                time.sleep(0.05)
            except Exception:
                break
        return ""

    def safe_clipboard_set(self, text: str) -> None:
        """Write text to clipboard with retry on TclError (AGENTS.md Rule 14)."""
        for _ in range(5):
            try:
                self.clipboard_clear()
                self.clipboard_append(text)
                self.update_idletasks()
                return
            except tk.TclError:
                time.sleep(0.05)
            except Exception:
                break

    # -------------------------------------------------------------------------
    # Global Exception Hooks & Exit Lifecycle
    # -------------------------------------------------------------------------
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

        # Sweep pending after jobs first (BUG-32)
        try:
            for job_id in self.tk.call("after", "info"):
                try:
                    self.after_cancel(job_id)
                except Exception:
                    pass
        except Exception:
            pass

        self.logger.info("UI / Theme / Config", "Saving configuration on exit...")
        self._save_user_prefs(silent=True)
        self._cleanup_drag_and_drop()
        self.destroy()

    def _on_root_destroy(self, event: tk.Event) -> None:
        if event.widget is self:
            self._destroyed = True
            try:
                for job_id in self.tk.call("after", "info"):
                    try:
                        self.after_cancel(job_id)
                    except Exception:
                        pass
            except Exception:
                pass
            if hasattr(self, "_search_poll_job") and self._search_poll_job:
                try:
                    self.after_cancel(self._search_poll_job)
                except Exception:
                    pass
                self._search_poll_job = None
            if hasattr(self, "_mtl_poll_job") and self._mtl_poll_job:
                try:
                    self.after_cancel(self._mtl_poll_job)
                except Exception:
                    pass
                self._mtl_poll_job = None
            if hasattr(self, "_mtl_drawer_poll_id") and self._mtl_drawer_poll_id:
                try:
                    self.after_cancel(self._mtl_drawer_poll_id)
                except Exception:
                    pass
                self._mtl_drawer_poll_id = None
            if hasattr(self, "_xuat_index_cancel") and self._xuat_index_cancel is not None:
                try:
                    self._xuat_index_cancel.set()
                except Exception:
                    pass
                self._xuat_index_cancel = None
            if hasattr(self, "_xuat_index_poll_id") and self._xuat_index_poll_id:
                try:
                    self.after_cancel(self._xuat_index_poll_id)
                except Exception:
                    pass
                self._xuat_index_poll_id = None
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
        # Sweep all pending Tk after jobs first (BUG-32)
        try:
            for job_id in self.tk.call("after", "info"):
                try:
                    self.after_cancel(job_id)
                except Exception:
                    pass
        except Exception:
            pass

        if hasattr(self, "_search_poll_job") and self._search_poll_job:
            try:
                self.after_cancel(self._search_poll_job)
            except Exception:
                pass
            self._search_poll_job = None
        if hasattr(self, "_mtl_poll_job") and self._mtl_poll_job:
            try:
                self.after_cancel(self._mtl_poll_job)
            except Exception:
                pass
            self._mtl_poll_job = None
        if hasattr(self, "_mtl_drawer_poll_id") and self._mtl_drawer_poll_id:
            try:
                self.after_cancel(self._mtl_drawer_poll_id)
            except Exception:
                pass
            self._mtl_drawer_poll_id = None
        if hasattr(self, "_xuat_index_cancel") and self._xuat_index_cancel is not None:
            try:
                self._xuat_index_cancel.set()
            except Exception:
                pass
            self._xuat_index_cancel = None
        if hasattr(self, "_xuat_index_poll_id") and self._xuat_index_poll_id:
            try:
                self.after_cancel(self._xuat_index_poll_id)
            except Exception:
                pass
            self._xuat_index_poll_id = None
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
        try:
            super().destroy()
        finally:
            # Terminate background logger last inside safe try/except (BUG-32)
            if hasattr(self, "logger") and self.logger:
                try:
                    self.logger.close()
                except Exception:
                    pass

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
                if isinstance(raw.get("show_ngui_ribbon"), bool):
                    self._saved_show_ngui_ribbon = raw["show_ngui_ribbon"]
                if isinstance(raw.get("mtl_drawer_enabled_engines"), dict):
                    defaults = {
                        "XUAT Cache": True,
                        "Google": True,
                        "DeepL": False,
                        "Local / Sugoi": False,
                        "LLM / OpenAI": False,
                    }
                    for eng_name in defaults:
                        val = raw["mtl_drawer_enabled_engines"].get(eng_name)
                        if isinstance(val, bool):
                            defaults[eng_name] = val
                    self._mtl_drawer_enabled_engines = defaults
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
                "show_ngui_ribbon": bool(self.var_show_ngui_ribbon.get()) if hasattr(self, "var_show_ngui_ribbon") else getattr(self, "_saved_show_ngui_ribbon", True),
                "mtl_drawer_enabled_engines": dict(getattr(self, "_mtl_drawer_enabled_engines", {})),
            }
            # In-memory serialization before file write ensures DPAPISecurityError never truncates config (BUG-33)
            encoded_payload = json.dumps(payload, indent=2, ensure_ascii=False)
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = CONFIG_PATH.with_suffix(".json.tmp")
            tmp_path.write_text(encoded_payload, encoding="utf-8")
            os.replace(tmp_path, CONFIG_PATH)
            if not silent:
                self.logger.debug("UI / Theme / Config", f"Saved config to {CONFIG_PATH}")
        except DPAPISecurityError as sec_err:
            self.logger.error("UI / Theme / Config", f"DPAPI security failure: {sec_err}. Preferences save aborted to prevent secret leakage.")
            if not silent:
                try:
                    self.show_toast("Security Error: Failed to encrypt credentials. Save aborted.", is_error=True)
                except Exception:
                    pass
            return
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
            self._apply_gutter_overflow_tag(self.gutter_clean)
        if hasattr(self, "gutter_cont"):
            self.gutter_cont.configure(bg=gutter_bg, fg=gutter_fg)
        if hasattr(self, "ruler_clean"):
            self.ruler_clean.configure(bg=gutter_bg)
        if hasattr(self, "ruler_cont"):
            self.ruler_cont.configure(bg=gutter_bg)

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
        self._apply_overflow_highlights(self.txt_dialogue)
        self._redraw_pixel_rulers()

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

        if hasattr(self, "_apply_mtl_all_script_theme_tags"):
            self._apply_mtl_all_script_theme_tags()

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

    def _sweep_cstyle_tags(self, widget: Optional[tk.Text]) -> None:
        """Delete all cached compiled NGUI style tags (`cstyle_*`) from `widget` (GEM-E03)."""
        if not widget or not widget.winfo_exists():
            return
        for tag_name in list(widget.tag_names()):
            if tag_name.startswith("cstyle_"):
                widget.tag_delete(tag_name)

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
        ov_bg = "#4a1c24" if not self._is_light_theme() else "#ffd6dc"
        ov_fg = best_contrast_fg(
            ov_bg,
            "#ff8fa3" if not self._is_light_theme() else "#9b111e",
            "#ffffff" if not self._is_light_theme() else "#1a1a1a",
        )
        widget.tag_configure(
            "line_overflow",
            background=ov_bg,
            foreground=ov_fg,
            underline=True,
        )
        widget.tag_configure(
            "search_hit",
            background=t["highlight_bg"],
            foreground=hl_fg,
            underline=True,
        )
        self._sweep_cstyle_tags(widget)
        widget.tag_raise("line_overflow")
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

