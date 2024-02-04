import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { KeywordAnalysis } from '../models/keywordAnalysis';
import { SubTitleSubctract } from '../models/subTitleSubctract';
@Injectable({
    providedIn: 'any',
})
export class ClippingService {

    public baseUrl: string = "http://127.0.0.1:5000/";
    constructor(protected http: HttpClient) {
    }

    get(url: string, body: any) {
        debugger
        return this.http.get(this.baseUrl + url, body);
    }

    post(url: string, data: any) {
        return this.http.post(this.baseUrl + url, data);
    }
}

