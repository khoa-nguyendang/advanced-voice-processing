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
    errorMessage = '';
    processing = false;
    detectedText = '';
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
                responseType: 'blob',
                observe: 'response'
            });

            upload$.subscribe({
                next: (res: any) => { 
                    console.info(res); 
                    this.detectedText = res.headers.get('X-Text'); 
                    this.playBlob(res.body); },
                error: (error: any) => {
                    console.log(error)
                    this.errorMessage = error;
                    this.processing = false;
                },
                complete: () => { this.processing = false; }
            });
        }
    }

    onErrorReceivingBuffer(err: any) {
        this.errorMessage = err;
    }

    playBlob(blob: Blob) {
        let el = this.audioResult?.nativeElement as HTMLAudioElement;
        el.src = URL.createObjectURL(blob);
        el.load();
        el.play();
    }
}
