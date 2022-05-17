/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

var apigClientFactory = {};
apigClientFactory.newClient = function (config) {
    var apigClient = { };
    if(config === undefined) {
        config = {
            accessKey: '',
            secretKey: '',
            sessionToken: '',
            region: '',
            apiKey: undefined,
            defaultContentType: 'application/json',
            defaultAcceptType: 'application/json'
        };
    }
    if(config.accessKey === undefined) {
        config.accessKey = '';
    }
    if(config.secretKey === undefined) {
        config.secretKey = '';
    }
    if(config.apiKey === undefined) {
        config.apiKey = '';
    }
    if(config.sessionToken === undefined) {
        config.sessionToken = '';
    }
    if(config.region === undefined) {
        config.region = 'us-east-1';
    }
    //If defaultContentType is not defined then default to application/json
    if(config.defaultContentType === undefined) {
        config.defaultContentType = 'application/json';
    }
    //If defaultAcceptType is not defined then default to application/json
    if(config.defaultAcceptType === undefined) {
        config.defaultAcceptType = 'application/json';
    }

    
    // extract endpoint and path from url
    var invokeUrl = 'https://v8w02mqq0e.execute-api.us-east-1.amazonaws.com/Beta0_23_Apr';
    var endpoint = /(^https?:\/\/[^\/]+)/g.exec(invokeUrl)[1];
    var pathComponent = invokeUrl.substring(endpoint.length);

    var sigV4ClientConfig = {
        accessKey: config.accessKey,
        secretKey: config.secretKey,
        sessionToken: config.sessionToken,
        serviceName: 'execute-api',
        region: config.region,
        endpoint: endpoint,
        defaultContentType: config.defaultContentType,
        defaultAcceptType: config.defaultAcceptType
    };

    var authType = 'NONE';
    if (sigV4ClientConfig.accessKey !== undefined && sigV4ClientConfig.accessKey !== '' && sigV4ClientConfig.secretKey !== undefined && sigV4ClientConfig.secretKey !== '') {
        authType = 'AWS_IAM';
    }

    var simpleHttpClientConfig = {
        endpoint: endpoint,
        defaultContentType: config.defaultContentType,
        defaultAcceptType: config.defaultAcceptType
    };

    var apiGatewayClient = apiGateway.core.apiGatewayClientFactory.newClient(simpleHttpClientConfig, sigV4ClientConfig);
    
    
    
    apigClient.getuserGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var getuserGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/getuser').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(getuserGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.getuserOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var getuserOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/getuser').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(getuserOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.getuserUseruiGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var getuserUseruiGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/getuser/userui').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(getuserUseruiGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.getuserUseruiOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var getuserUseruiOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/getuser/userui').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(getuserUseruiOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.placeLiveForecastGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['compoundCode', 'name', 'vicinity'], ['body']);
        
        var placeLiveForecastGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/placeLiveForecast').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['compoundCode', 'name', 'vicinity']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(placeLiveForecastGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.placeLiveForecastOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var placeLiveForecastOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/placeLiveForecast').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(placeLiveForecastOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.placedetailGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['placeType', 'username', 'placeId'], ['body']);
        
        var placedetailGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/placedetail').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['placeType', 'username', 'placeId']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(placedetailGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.placedetailOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var placedetailOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/placedetail').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(placedetailOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.placeinterestedGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['username', 'placeId'], ['body']);
        
        var placeinterestedGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/placeinterested').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['username', 'placeId']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(placeinterestedGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.placeinterestedOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var placeinterestedOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/placeinterested').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(placeinterestedOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.placereviewsGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['username', 'place_id', 'comment', 'rating'], ['body']);
        
        var placereviewsGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/placereviews').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['username', 'place_id', 'comment', 'rating']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(placereviewsGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.placereviewsOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var placereviewsOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/placereviews').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(placereviewsOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.placesNearbySearchGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['currentLong', 'username', 'openNow', 'minPrice', 'textLocation', 'placeType', 'radius', 'rankBy', 'useCurrentLocation', 'currentLat', 'maxPrice', 'numResults'], ['body']);
        
        var placesNearbySearchGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/placesNearbySearch').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['currentLong', 'username', 'openNow', 'minPrice', 'textLocation', 'placeType', 'radius', 'rankBy', 'useCurrentLocation', 'currentLat', 'maxPrice', 'numResults']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(placesNearbySearchGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.placesNearbySearchOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var placesNearbySearchOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/placesNearbySearch').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(placesNearbySearchOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.useruiPost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var useruiPostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/userui').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(useruiPostRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.useruiOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var useruiOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/userui').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(useruiOptionsRequest, authType, additionalParams, config.apiKey);
    };
    

    return apigClient;
};
