# BUNDLE references (16/18) | Files: references/misora_parts/misora_part10_L13098-L14559.py

--- FILE: references/misora_parts/misora_part10_L13098-L14559.py [PART 2 | L1444-1465/1465 | SHA:19f9975ac826] ---
                        new_text=new_text,
                        file_path=str(self.current_file_path) if self.current_file_path else "",
                        box_uid=b_uid,
                        source="mtl",
                        old_seg_texts=old_segs,
                        new_seg_texts=new_segs,
                    )
                )
                self._modified_boxes.add(b_idx)
                applied_count += 1
        finally:
            self.undo_journal.end_batch()

        if applied_count > 0:
            self._mark_document_dirty(self.current_file_path)
            self._dirty_state_changed()
            self._update_views()
            self.show_toast(f"✓ Applied {eng} translations to {applied_count} box(es)")
        else:
            self.show_toast("No translations were applied.")
        return applied_count

