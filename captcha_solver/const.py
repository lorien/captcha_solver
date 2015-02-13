SOLVER_BACKEND_ALIAS = {
    'antigate': 'captcha_solver.captcha_backend.antigate.AntigateBackend',
    'browser': 'captcha_solver.captcha_backend.browser.BrowserBackend',
    'gui': 'captcha_solver.captcha_backend.gui.GuiBackend',
}

TRANSPORT_BACKEND_ALIAS = {
    'grab': 'captcha_solver.transport_backend.grab_backend.GrabBackend',
    'urllib': 'captcha_solver.transport_backend.urllib_backend.UrllibBackend'
}
