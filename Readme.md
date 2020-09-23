# Readme

Plugin to download DOI metadata from the [ Crossref API ]( https://github.com/CrossRef/rest-api-doc ).

*Note* this is in an early stage. Consider it as early alpha. 

## Notes
The provided bibliographic metadata is quite complex. 
Unfortunately Calibre only supports setting the default columns in a metadata plugin ([see](https://www.mobileread.com/forums/showpost.php?p=4025488&postcount=2)) 

Currently, additional information is dumped into the comment field.

### Crossref

I'm not affiliated with Crossref.
I'm not sure about the status of [ Crossref API ](https://github.com/CrossRef/rest-api-doc).  
I keep experiencing following issues:
 - Many of my queries go frustratingly slow or time out.
 - The query results also hold some fields not documented in [api format documentation](https://github.com/Crossref/rest-api-doc/blob/master/api_format.md).
 -  I keep receiving `503 Service unavailable` responses.
 
Relevant facts:
 - There is a [service status page](http://status.crossref.org/)
 - They have "polite servers" that require one to provide a contact email.
 - They ramble about needing this for reliable service.

The whole idea that requiring to add an email address to improve the service seems suspicious.
I mean it's easy enough to automatically generate one - so spammers won't be limited, but as real person I'd fear my address might get abused.
I also think that such search requests contain sensitive information, so I definitely would not want that to be linked by default with a personal identification.
For the same reason I don't intend setting a user agent for such requests.

Currently I submit my requests manually - usually spaced few minutes apart.
I manage to get one response after about a minute, with some 503 errors mixed in.
I don't see how this would justify any blocking.
The only reason I can imagine is they are sending all anonymous requests into a tar pit.
With this response time it is all but useless for my intended application to retrieve DOIs for dozen or even 100s of references.

There are no plans to implement the API for the paid "Metadata Plus" service.

