#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib
import subprocess
import threading

class RuneInstaller(Adw.Application):
    def __init__(self):
        super().__init__(application_id='dev.runeos.installer')
        self.connect('activate', self.on_activate)
        self.selected_bundles = set()

    def on_activate(self, app):
        self.win = Adw.ApplicationWindow(application=app)
        self.win.set_title("Rune OS Installer")
        self.win.set_default_size(800, 550)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
        self.win.set_content(self.stack)
        self.build_welcome_page()
        self.build_bundles_page()
        self.build_user_page()
        self.build_install_page()
        self.stack.set_visible_child_name('welcome')
        self.win.present()

    def nav_box(self, back_cb=None, next_cb=None, next_label="Next →"):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        box.set_margin_top(16)
        if back_cb:
            btn = Gtk.Button(label="← Back")
            btn.connect('clicked', back_cb)
            box.append(btn)
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        box.append(spacer)
        if next_cb:
            btn = Gtk.Button(label=next_label)
            btn.add_css_class('suggested-action')
            btn.connect('clicked', next_cb)
            box.append(btn)
        return box

    def build_welcome_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_margin_top(60)
        box.set_margin_bottom(32)
        box.set_margin_start(60)
        box.set_margin_end(60)
        logo = Gtk.Label(label="ᚱ")
        logo.add_css_class('title-1')
        box.append(logo)
        title = Gtk.Label(label="Welcome to Rune OS")
        title.add_css_class('title-1')
        title.set_margin_top(16)
        box.append(title)
        sub = Gtk.Label(label="Minimal. Fast. Built for developers on ARM.")
        sub.add_css_class('dim-label')
        sub.set_margin_top(8)
        box.append(sub)
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        box.append(spacer)
        box.append(self.nav_box(
            next_cb=lambda b: self.stack.set_visible_child_name('bundles'),
            next_label="Get Started →"
        ))
        self.stack.add_named(box, 'welcome')

    def build_bundles_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_margin_top(32)
        box.set_margin_bottom(32)
        box.set_margin_start(60)
        box.set_margin_end(60)
        title = Gtk.Label(label="Choose your stack")
        title.add_css_class('title-2')
        title.set_halign(Gtk.Align.START)
        box.append(title)
        sub = Gtk.Label(label="Only selected packages will be installed. Add more anytime with: rune bundle install")
        sub.add_css_class('dim-label')
        sub.set_halign(Gtk.Align.START)
        sub.set_margin_top(4)
        sub.set_margin_bottom(20)
        box.append(sub)
        grid = Gtk.Grid()
        grid.set_column_spacing(12)
        grid.set_row_spacing(12)
        grid.set_column_homogeneous(True)
        bundles = [
            ("🌐", "Web / Fullstack",  "Node, Python, PHP, Nginx",     "web"),
            ("🔧", "Systems / C++",    "gcc, clang, cmake, gdb",        "systems"),
            ("☕", "Java",             "OpenJDK 21, Maven, Gradle",     "java"),
            ("🗄️",  "Databases",        "MySQL + MongoDB",               "databases"),
            ("🧠", "AI / ML",          "PyTorch, Jupyter, NumPy",       "ai-ml"),
            ("🐳", "DevOps / Cloud",   "Docker, Ansible, kubectl",      "devops"),
            ("🦀", "Rust / Go",        "rustup, cargo, go",             "rust-go"),
            ("🤖", "AI Tools",         "Ollama + Llama 3.2 offline",    "ai-tools"),
        ]
        self.bundle_checks = {}
        for i, (icon, name, desc, key) in enumerate(bundles):
            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            card.set_margin_top(8)
            card.set_margin_bottom(8)
            card.set_margin_start(8)
            card.set_margin_end(8)
            top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            top.append(Gtk.Label(label=icon))
            name_label = Gtk.Label(label=name)
            name_label.add_css_class('heading')
            name_label.set_hexpand(True)
            name_label.set_halign(Gtk.Align.START)
            top.append(name_label)
            check = Gtk.CheckButton()
            self.bundle_checks[key] = check
            top.append(check)
            card.append(top)
            desc_label = Gtk.Label(label=desc)
            desc_label.add_css_class('dim-label')
            desc_label.set_halign(Gtk.Align.START)
            card.append(desc_label)
            frame = Gtk.Frame()
            frame.set_child(card)
            grid.attach(frame, i % 2, i // 2, 1, 1)
        box.append(grid)
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        box.append(spacer)
        box.append(self.nav_box(
            back_cb=lambda b: self.stack.set_visible_child_name('welcome'),
            next_cb=lambda b: self.stack.set_visible_child_name('user'),
        ))
        self.stack.add_named(box, 'bundles')

    def build_user_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_margin_top(60)
        box.set_margin_bottom(32)
        box.set_margin_start(80)
        box.set_margin_end(80)
        title = Gtk.Label(label="Create your account")
        title.add_css_class('title-2')
        title.set_halign(Gtk.Align.START)
        box.append(title)
        sub = Gtk.Label(label="This will be your user on Rune OS.")
        sub.add_css_class('dim-label')
        sub.set_halign(Gtk.Align.START)
        sub.set_margin_top(4)
        sub.set_margin_bottom(24)
        box.append(sub)
        self.username_entry = Gtk.Entry()
        self.username_entry.set_placeholder_text("Username")
        self.username_entry.set_margin_bottom(12)
        box.append(self.username_entry)
        self.password_entry = Gtk.Entry()
        self.password_entry.set_placeholder_text("Password")
        self.password_entry.set_visibility(False)
        self.password_entry.set_margin_bottom(12)
        box.append(self.password_entry)
        self.hostname_entry = Gtk.Entry()
        self.hostname_entry.set_placeholder_text("Hostname (e.g. my-rune-machine)")
        box.append(self.hostname_entry)
        self.error_label = Gtk.Label(label="")
        self.error_label.add_css_class('error')
        self.error_label.set_margin_top(8)
        box.append(self.error_label)
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        box.append(spacer)
        box.append(self.nav_box(
            back_cb=lambda b: self.stack.set_visible_child_name('bundles'),
            next_cb=self.validate_and_install,
            next_label="Install Rune OS →"
        ))
        self.stack.add_named(box, 'user')

    def build_install_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        box.set_margin_top(60)
        box.set_margin_bottom(32)
        box.set_margin_start(60)
        box.set_margin_end(60)
        box.set_valign(Gtk.Align.CENTER)
        self.install_title = Gtk.Label(label="Installing Rune OS...")
        self.install_title.add_css_class('title-2')
        box.append(self.install_title)
        self.install_sub = Gtk.Label(label="Please wait...")
        self.install_sub.add_css_class('dim-label')
        box.append(self.install_sub)
        self.progress = Gtk.ProgressBar()
        self.progress.set_margin_top(16)
        box.append(self.progress)
        self.log_view = Gtk.TextView()
        self.log_view.set_editable(False)
        self.log_view.set_monospace(True)
        self.log_view.set_margin_top(16)
        self.log_buffer = self.log_view.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_child(self.log_view)
        scroll.set_vexpand(True)
        box.append(scroll)
        self.stack.add_named(box, 'install')

    def validate_and_install(self, btn):
        username = self.username_entry.get_text().strip()
        password = self.password_entry.get_text()
        hostname = self.hostname_entry.get_text().strip()
        if not username:
            self.error_label.set_label("Username cannot be empty.")
            return
        if not password:
            self.error_label.set_label("Password cannot be empty.")
            return
        if not hostname:
            self.error_label.set_label("Hostname cannot be empty.")
            return
        if ' ' in username:
            self.error_label.set_label("Username cannot contain spaces.")
            return
        selected = [k for k, v in self.bundle_checks.items() if v.get_active()]
        if not selected:
            selected = ['core']
        bundles_str = ','.join(selected)
        self.stack.set_visible_child_name('install')
        thread = threading.Thread(
            target=self.run_install,
            args=(username, password, hostname, bundles_str),
            daemon=True
        )
        thread.start()
        GLib.timeout_add(300, self.pulse_progress)

    def run_install(self, username, password, hostname, bundles):
        steps = [
            ("Setting hostname...",       f"echo {hostname} > /etc/hostname"),
            ("Creating user account...",  f"useradd -m -s /bin/bash -G sudo {username} && echo '{username}:{password}' | chpasswd"),
            ("Copying default configs...", f"cp -r /etc/skel/. /home/{username}/ && chown -R {username}:{username} /home/{username}"),
            ("Enabling services...",      "systemctl enable sddm NetworkManager 2>/dev/null || true"),
        ]
        total = len(steps)
        for i, (msg, cmd) in enumerate(steps):
            GLib.idle_add(self.update_status, msg, i / total)
            try:
                subprocess.run(cmd, shell=True, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                GLib.idle_add(self.log_line, f"Warning: {e}")
        if bundles and bundles != 'core':
            GLib.idle_add(self.update_status, "Installing selected bundles...", 0.6)
            for bundle in bundles.split(','):
                try:
                    subprocess.run(
                        ['pkexec', '/usr/local/bin/rune', 'bundle', 'install', bundle],
                        check=True
                    )
                    GLib.idle_add(self.log_line, f"✓ {bundle} installed")
                except Exception as e:
                    GLib.idle_add(self.log_line, f"Warning: {bundle} - {e}")
        GLib.idle_add(self.install_done)

    def update_status(self, msg, fraction):
        self.install_sub.set_label(msg)
        self.progress.set_fraction(fraction)
        self.log_line(msg)

    def log_line(self, text):
        end = self.log_buffer.get_end_iter()
        self.log_buffer.insert(end, text + "\n")

    def pulse_progress(self):
        current = self.progress.get_fraction()
        if current < 0.95 and self.install_title.get_label() == "Installing Rune OS...":
            self.progress.set_fraction(min(current + 0.005, 0.95))
            return True
        return False

    def install_done(self):
        self.progress.set_fraction(1.0)
        self.install_title.set_label("✓ Rune OS Installed!")
        self.install_sub.set_label("Restart your machine to boot into Rune OS.")
        self.log_line("==> Installation complete!")

app = RuneInstaller()
app.run()
