import { Component, OnDestroy } from '@angular/core';
import { generateMeetingReport, formatReportAsTxt, MeetingReport } from '../../core/utils/meeting-report';
import { filterOffensiveWords } from '../../core/utils/offensive-filter';

@Component({
  selector: 'app-voice-notes',
  standalone: false,
  templateUrl: './voice-notes.component.html',
  styleUrls: ['./voice-notes.component.scss'],
})
export class VoiceNotesComponent implements OnDestroy {
  isRecording = false;
  browserSupported = true;
  transcript = '';
  interimText = '';
  view: 'transcript' | 'report' = 'transcript';
  report: MeetingReport | null = null;
  elapsedSeconds = 0;
  exportedTxt = false;

  private recognition: any = null;
  private timerRef: any = null;

  constructor() {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) {
      this.browserSupported = false;
      return;
    }

    this.recognition = new SR();
    this.recognition.lang = 'es-CO';
    this.recognition.continuous = true;
    this.recognition.interimResults = true;
    this.recognition.maxAlternatives = 1;

    this.recognition.onresult = (event: any) => {
      let interim = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const res = event.results[i];
        const rawText: string = res[0].transcript;
        if (res.isFinal) {
          const clean = filterOffensiveWords(rawText.trim());
          this.transcript += (this.transcript ? ' ' : '') + clean;
        } else {
          interim += rawText;
        }
      }
      this.interimText = interim;
    };

    this.recognition.onerror = (event: any) => {
      // Ignore 'aborted' errors (triggered when we stop manually)
      if (event.error !== 'aborted' && event.error !== 'no-speech') {
        console.warn('Speech recognition error:', event.error);
      }
    };

    // Auto-restart when browser stops recognition (happens every ~60s in Chrome)
    this.recognition.onend = () => {
      if (this.isRecording) {
        try { this.recognition.start(); } catch { /* already started */ }
      }
    };
  }

  toggleRecording(): void {
    this.isRecording ? this.stopRecording() : this.startRecording();
  }

  startRecording(): void {
    if (!this.browserSupported) return;
    this.isRecording = true;
    this.elapsedSeconds = 0;
    try {
      this.recognition.start();
    } catch { /* recognition already running */ }
    this.timerRef = setInterval(() => this.elapsedSeconds++, 1000);
  }

  stopRecording(): void {
    this.isRecording = false;
    clearInterval(this.timerRef);
    // Commit any interim text captured before the browser stops the session
    if (this.interimText.trim()) {
      const clean = filterOffensiveWords(this.interimText.trim());
      this.transcript += (this.transcript ? ' ' : '') + clean;
    }
    this.interimText = '';
    try { this.recognition.stop(); } catch { /* already stopped */ }
  }

  generateReport(): void {
    if (!this.transcript.trim()) return;
    this.report = generateMeetingReport(this.transcript);
    this.view = 'report';
  }

  exportTxt(): void {
    if (!this.transcript) return;
    this.downloadFile(this.transcript, `transcripcion_${this.fileDateStamp()}.txt`);
    this.exportedTxt = true;
    setTimeout(() => (this.exportedTxt = false), 2000);
  }

  exportReportTxt(): void {
    if (!this.report) return;
    this.downloadFile(formatReportAsTxt(this.report), `informe_reunion_${this.fileDateStamp()}.txt`);
  }

  clearTranscript(): void {
    if (this.isRecording) this.stopRecording();
    this.transcript = '';
    this.interimText = '';
    this.report = null;
    this.view = 'transcript';
    this.elapsedSeconds = 0;
  }

  formatTime(seconds: number): string {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }

  get wordCount(): number {
    return this.transcript.split(/\s+/).filter(w => w.length > 0).length;
  }

  private downloadFile(content: string, filename: string): void {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  private fileDateStamp(): string {
    return new Date().toISOString().slice(0, 16).replace(/[T:]/g, '-');
  }

  ngOnDestroy(): void {
    if (this.isRecording) this.stopRecording();
    clearInterval(this.timerRef);
  }
}
