// macOS print check: prints a JoRoScope report through WebKit's real print path (print CSS,
// A4) into a PDF, as Safari would. Start the server first, then:
//   swiftc -O scripts/print_pdf.swift -o /tmp/print_pdf
//   /tmp/print_pdf http://localhost:8765/ report.pdf complete ta south
// Presets: jathagam, detailed, complete. Chart styles: south, north, east, srilanka.
import AppKit
import WebKit

let args = CommandLine.arguments
let url = URL(string: args[1])!
let outPath = args[2]
let preset = args[3]
let lang = args[4]
let style = args[5]

final class Driver: NSObject, WKNavigationDelegate {
    let web: WKWebView
    let window: NSWindow
    init(_ web: WKWebView, _ window: NSWindow) { self.web = web; self.window = window }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 6) {
            let js = """
            (function() {
              if (!currentChart) return 'no chart';
              currentLang = '\(lang)';
              buildPrintReport('\(preset)', PRINT_PRESETS['\(preset)'].sections, '\(style)');
              document.body.classList.add('printing-jathagam');
              return 'ok ' + document.querySelectorAll('#print-jathagam .pj-section').length;
            })()
            """
            webView.evaluateJavaScript(js) { result, error in
                FileHandle.standardError.write("build: \(String(describing: result)) \(String(describing: error))\n".data(using: .utf8)!)
                DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) { self.printPDF() }
            }
        }
    }

    func printPDF() {
        let info = NSPrintInfo.shared.copy() as! NSPrintInfo
        info.paperSize = NSSize(width: 595.28, height: 841.89)
        info.topMargin = 0; info.bottomMargin = 0; info.leftMargin = 0; info.rightMargin = 0
        info.jobDisposition = .save
        info.dictionary()[NSPrintInfo.AttributeKey.jobSavingURL] = URL(fileURLWithPath: outPath)
        let op = web.printOperation(with: info)
        op.showsPrintPanel = false
        op.showsProgressPanel = false
        op.view?.frame = NSRect(x: 0, y: 0, width: 595, height: 842)
        op.runModal(for: window, delegate: self, didRun: #selector(done(_:success:contextInfo:)), contextInfo: nil)
    }

    @objc func done(_ op: NSPrintOperation, success: Bool, contextInfo: UnsafeMutableRawPointer?) {
        FileHandle.standardError.write("printed: \(success)\n".data(using: .utf8)!)
        NSApp.terminate(nil)
    }
}

let app = NSApplication.shared
app.setActivationPolicy(.prohibited)
let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 1200, height: 900), styleMask: [.titled], backing: .buffered, defer: false)
let web = WKWebView(frame: window.contentView!.bounds)
window.contentView!.addSubview(web)
let driver = Driver(web, window)
web.navigationDelegate = driver
web.load(URLRequest(url: url))
DispatchQueue.main.asyncAfter(deadline: .now() + 60) {
    FileHandle.standardError.write("timeout\n".data(using: .utf8)!)
    exit(2)
}
app.run()
