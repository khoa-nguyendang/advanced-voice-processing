import { AsyncPipe, NgClass, NgForOf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
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
    MatIconModule
  ],
})
export class AudioTranslateComponent {
    fileName = '';

    constructor(private http: HttpClient) {}

    onFileSelected(event: any) {

        const file:File = event.target.files[0];

        if (file) {

            this.fileName = file.name;

            const formData = new FormData();

            formData.append("file", file);
            formData.append("speaker", "khoaspeech");

            const upload$ = this.http.post("/voice-translate", formData);

            upload$.subscribe();
        }
    }
}
