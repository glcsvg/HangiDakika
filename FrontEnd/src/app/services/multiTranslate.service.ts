import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { MultiTranslate } from '../models/multiTranslate';
@Injectable({
    providedIn: 'any',
})
export class MultiTranslateService {

    public baseUrl: string = "http://127.0.0.1:5000/";
    constructor(protected http: HttpClient) {
    }

    get(url: string, body: any) {
        return this.http.get<MultiTranslate>(this.baseUrl + url, body);
    }

    post(url: string, data: any): Observable<MultiTranslate> {
        return this.http.post<MultiTranslate>(this.baseUrl + url, data);
    }
}
