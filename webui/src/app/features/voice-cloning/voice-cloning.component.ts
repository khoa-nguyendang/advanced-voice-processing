import { AsyncPipe, CommonModule, NgClass, NgForOf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, ElementRef, ViewChild } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { ArticleListComponent } from 'src/app/shared/article-helpers/article-list.component';

@Component({
    selector: 'app-voice-cloning',
    templateUrl: './voice-cloning.component.html',
    styleUrls: ['./voice-cloning.component.css'],
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
export class VoiceCloningComponent {
    audioFile: File | undefined;
    speakerAudioFile: File | undefined;
    fileName = '';
    fileNameSpeaker = '';
    errorMessage = '';
    processing = false;
    @ViewChild('audioResult') audioResult: ElementRef<HTMLAudioElement> | undefined;

    constructor(private http: HttpClient) { }

    onSubmit(event: any) {
        event.preventDefault();
        if (!this.audioFile) {
            alert("You must be upload Audio file (.wma)");
            return;
        }

        if (!this.speakerAudioFile) {
            alert("You must be upload audio of Speaker file (.wma)");
            return;
        }

        this.processing = true;
        const formData = new FormData();
        formData.append("file", this.audioFile);
        formData.append("speaker", this.speakerAudioFile);
        const upload$ = this.http.post("/voice-clone", formData, {
            responseType: 'blob'
        });

        upload$.subscribe({
            next: (res: any) => { this.playBlob(res); },
            error: (error: any) => {
                console.log(error)
                this.errorMessage = error;
                this.processing = false;
            },
            complete: () => { this.processing = false; }
        });
    }

    onFileSelected(event: any) {
        let file: File = event.target.files[0];
        this.audioFile = file;
        this.fileName = file.name;
    }

    onFileSpeakerSelected(event: any) {
        let file: File = event.target.files[0];
        this.speakerAudioFile = file;
        this.fileNameSpeaker = file.name;
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
