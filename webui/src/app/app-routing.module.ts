import { inject, NgModule } from "@angular/core";
import { PreloadAllModules, RouterModule, Routes } from "@angular/router";
import { map } from "rxjs/operators";
import { UserService } from "./core/services/user.service";
import { ProfileComponent } from "./features/profile/profile.component";

const routes: Routes = [
  {
    path: "",
    loadComponent: () =>
      import("./features/home/home.component").then((m) => m.HomeComponent),
  },
  {
    path: "voice-cloning",
    loadComponent: () => import("./features/voice-cloning/voice-cloning.component").then((m) => m.VoiceCloningComponent),
  },
  {
    path: "audio-transcribe",
    loadComponent: () => import("./features/audio-transcribe/audio-transcribe.component").then((m) => m.AudioTranscribeComponent),
  },
  {
    path: "audio-translate",
    loadComponent: () => import("./features/audio-translate/audio-translate.component").then((m) => m.AudioTranslateComponent),
  },
  {
    path: "login",
    loadComponent: () =>
      import("./core/auth/auth.component").then((m) => m.AuthComponent),
    canActivate: [
      () => inject(UserService).isAuthenticated.pipe(map((isAuth) => !isAuth)),
    ],
  },
  {
    path: "register",
    loadComponent: () =>
      import("./core/auth/auth.component").then((m) => m.AuthComponent),
    canActivate: [
      () => inject(UserService).isAuthenticated.pipe(map((isAuth) => !isAuth)),
    ],
  },
  {
    path: "settings",
    loadComponent: () =>
      import("./features/settings/settings.component").then(
        (m) => m.SettingsComponent
      ),
    canActivate: [() => inject(UserService).isAuthenticated],
  },
  {
    path: "profile",
    children: [
      {
        path: ":username",
        component: ProfileComponent,
        children: [
          {
            path: "",
            loadComponent: () =>
              import("./features/profile/profile-articles.component").then(
                (m) => m.ProfileArticlesComponent
              ),
          },
          {
            path: "favorites",
            loadComponent: () =>
              import("./features/profile/profile-favorites.component").then(
                (m) => m.ProfileFavoritesComponent
              ),
          },
        ],
      },
    ],
  },
  {
    path: "editor",
    children: [
      {
        path: "",
        loadComponent: () =>
          import("./features/editor/editor.component").then(
            (m) => m.EditorComponent
          ),
        canActivate: [() => inject(UserService).isAuthenticated],
      },
      {
        path: ":slug",
        loadComponent: () =>
          import("./features/editor/editor.component").then(
            (m) => m.EditorComponent
          ),
        canActivate: [() => inject(UserService).isAuthenticated],
      },
    ],
  },
  {
    path: "article/:slug",
    loadComponent: () =>
      import("./features/article/article.component").then(
        (m) => m.ArticleComponent
      ),
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      preloadingStrategy: PreloadAllModules,
    }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
