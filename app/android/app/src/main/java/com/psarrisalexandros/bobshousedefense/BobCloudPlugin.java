package com.psarrisalexandros.bobshousedefense;

import android.app.backup.BackupManager;
import android.content.Context;
import android.content.SharedPreferences;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/**
 * A copy of the save that Android backs up to the player's Google account.
 * It is written to one small preferences file, and that file is the only thing the backup rules include
 * (res/xml/backup_rules.xml and data_extraction_rules.xml). Android restores it when the game is installed again
 * or moved to a new phone. Nothing is backed up when the player has turned Android's backup off; the calls still succeed.
 */
@CapacitorPlugin(name = "BobCloud")
public class BobCloudPlugin extends Plugin {
    static final String FILE = "bob_cloud";

    private SharedPreferences prefs() {
        return getContext().getSharedPreferences(FILE, Context.MODE_PRIVATE);
    }

    @PluginMethod
    public void put(PluginCall call) {
        String key = call.getString("key"), value = call.getString("value");
        if (key == null || value == null) {
            call.reject("key and value are required");
            return;
        }
        prefs().edit().putString(key, value).apply();
        new BackupManager(getContext()).dataChanged();
        call.resolve();
    }

    @PluginMethod
    public void get(PluginCall call) {
        String key = call.getString("key");
        if (key == null) {
            call.reject("key is required");
            return;
        }
        String value = prefs().getString(key, null);
        JSObject out = new JSObject();
        if (value != null) out.put("value", value);
        call.resolve(out);
    }
}
