import { AsyncPipe, CommonModule, NgClass, NgForOf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { ArticleListComponent } from 'src/app/shared/article-helpers/article-list.component';

@Component({
  selector: 'app-audio-transcribe',
  templateUrl: './audio-transcribe.component.html',
  styleUrls: ['./audio-transcribe.component.css'],
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
export class AudioTranscribeComponent {
    fileName = '';
    text_result = '';
    processing = false;
    constructor(private http: HttpClient) {}

    onFileSelected(event: any) {

        const file:File = event.target.files[0];
        
        if (file) {
            this.processing = true;
            this.fileName = file.name;

            const formData = new FormData();

            formData.append("file", file);

            const upload$ = this.http.post("/voice-recognize", formData);

            upload$.subscribe({
                next: (res: any) => {
                    console.log(res);
                    this.text_result = res.data[0];
                },
                error: (error: any) => {
                    console.log(error);
                    this.processing = false;
                },
                complete: () => {this.processing = false;}
            });
        }
    }
}
