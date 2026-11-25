# BUNDLE references (6/18) | Files: references/misora_parts/misora_part05_L05666-L07163.py

--- FILE: references/misora_parts/misora_part05_L05666-L07163.py [PART 2 | L1453-1501/1501 | SHA:9a59a02d6153] ---
        self.lbl_status = self._tag_role(
            tk.Label(action_bar, text=getattr(self, "_default_status_text", "Ready. Drag & Drop or open a .unity3d bundle or folder to begin."), font=("Segoe UI", 9), bg=t["bg_panel"], fg=t["fg_muted"]),
            "label_muted"
        )
        self.lbl_status.pack(side="left", padx=8, pady=6)

        self.var_sync_xuat = tk.BooleanVar(master=self, value=True)
        cb_sync = ttk.Checkbutton(
            action_bar,
            text="Also update matching XUAT .txt dictionary on Save",
            variable=self.var_sync_xuat,
            style="Panel.TCheckbutton"
        )
        cb_sync.pack(side="right", padx=(8, 12))

        self.ico_revert = self.get_icon("revert", (15, 15))
        btn_revert = ttk.Button(action_bar, text=" Revert Box", image=self.ico_revert, compound="left", style="TButton", command=self.on_revert_box)
        btn_revert.pack(side="right", padx=4)

        self.ico_save = self.get_icon("save", (15, 15))
        self.btn_save = ttk.Button(action_bar, text=" Save & Patch Bundle (Ctrl+S)", image=self.ico_save, compound="left", style="Pink.TButton", command=self.on_save)
        self.btn_save.pack(side="right", padx=4)

    def _toggle_console_shortcut(self) -> None:
        """Inform user that diagnostic logs stream live to the standard Windows console."""
        self.show_toast("Logs stream to the persistent Windows console.")

    def _get_active_text_widget(self) -> Optional[tk.Text]:
        """Resolve the currently active or focused Text widget safely without aliasing (Rule 3)."""
        focused = self.focus_get()
        if isinstance(focused, tk.Text):
            return focused
        if getattr(self, "var_continuous_view", None) and self.var_continuous_view.get():
            if getattr(self, "is_box0_active", False) and hasattr(self, "_card_widgets") and -1 in self._card_widgets:
                card_txt = self._card_widgets[-1].get("txt")
                if card_txt and card_txt.winfo_exists():
                    return card_txt
            if hasattr(self, "_card_widgets") and self.current_box_idx in self._card_widgets:
                card_txt = self._card_widgets[self.current_box_idx].get("txt")
                if card_txt and card_txt.winfo_exists():
                    return card_txt
            if hasattr(self, "txt_continuous") and self.txt_continuous.winfo_exists():
                return self.txt_continuous
        if getattr(self, "is_box0_active", False) and hasattr(self, "txt_box0_summary") and self.txt_box0_summary.winfo_exists():
            return self.txt_box0_summary
        if hasattr(self, "txt_dialogue") and self.txt_dialogue.winfo_exists():
            return self.txt_dialogue
        return getattr(self, "txt_dialogue", None)

