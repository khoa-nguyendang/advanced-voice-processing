import { AsyncPipe, CommonModule, NgClass, NgForOf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, ElementRef, ViewChild } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { ArticleListComponent } from 'src/app/shared/article-helpers/article-list.component';

@Component({
    selector: 'app-audio-translate',
    templateUrl: './audio-translate.component.html',
    styleUrls: ['./audio-translate.component.css'],
    standalone: true,
    imports: [
        NgClass,
        ArticleListComponent,
        AsyncPipe,
        NgForOf,
        MatIconModule,
        CommonModule
    ],
})
export class AudioTranslateComponent {
    fileName = '';
    audioContext = new AudioContext();
    errorMessage = '';
    processing = false;
    @ViewChild('audioResult') audioResult: ElementRef<HTMLAudioElement> | undefined;

    constructor(private http: HttpClient) { }

    onFileSelected(event: any) {

        const file: File = event.target.files[0];

        if (file) {
            this.processing = true;
            this.fileName = file.name;

            const formData = new FormData();

            formData.append("file", file);
            formData.append("speaker", "khoaspeech");

            const upload$ = this.http.post("/voice-translate", formData, {
                responseType: 'blob'
            });

            upload$.subscribe({
                next: (res: any) => {
                    this.onReceivedBlob(res);
                },
                error: (error: any) => {
                    console.log(error)
                    this.errorMessage = error;
                },
                complete: () => { this.processing = false;}
            });
        }
    }

    onReceivedBlob(blob: Blob) {
        try {
            const audio = document.getElementById('audio_result') as HTMLAudioElement;
            // audio.src = URL.createObjectURL(blob);
            // audio.play();
            // return;
            let fileReader = new FileReader();
            let arrayBuffer: ArrayBuffer;
            fileReader.onloadend = () => {
                arrayBuffer = fileReader.result as ArrayBuffer;
                this.audioContext.decodeAudioData(arrayBuffer, this.playSound.bind(this), this.onErrorReceivingBuffer.bind(this));
            }
            fileReader.readAsArrayBuffer(blob);
        } catch (ex) {
            console.log(ex);
        }
    }

    onErrorReceivingBuffer(err: any) {
        this.errorMessage = err;
    }

    playSound(buffer: AudioBuffer) {
        let el = this.audioResult?.nativeElement as HTMLAudioElement;
        let elementSource = this.audioContext.createMediaElementSource(el);
        elementSource.connect(this.audioContext.destination);

        let source = this.audioContext.createBufferSource(); // creates a sound source
        source.buffer = buffer;                    // tell the source which sound to play
        source.connect(this.audioContext.destination);       // connect the source to the context's destination (the speakers)

        source.start(0);                          // play the source now
    }
}
