= Readme =

Plugin to download DOI metadata from the [ Crossref API ]( https://github.com/CrossRef/rest-api-doc ).

*Note* this is in an early stage. Consider it as early alpha. 

Based on the [calibre guides for plugins](https://manual.calibre-ebook.com/creating_plugins.html) and on the bundled `GoogleBooks` plugin.

The provided bibliographic metadata is quite complex. 
Unfortunately Calibre only supports setting the default columns in a metadata plugin ([see](https://www.mobileread.com/forums/showpost.php?p=4025488&postcount=2)) 

Currently, additional information is dumped into the comment field.

I'm not sure about the status of [ Crossref API ]( https://github.com/CrossRef/rest-api-doc ).  
I keep experiencing following issues:
 - Many of my queries go frustratingly slow or time out.
 - The query results also hold some fields not documented in [api format documentation](https://github.com/Crossref/rest-api-doc/blob/master/api_format.md).
 -  I keep receiving `503 Service unavailable` responses.
 
On 2020-09-23 the API description I was working with was gone from github.
A new API documentation appeared: https://github.com/CrossRef/rest-api-doc
Interestion additons were:
 - There is a [ service status page ](http://status.crossref.org/)
 - They have "polite servers" that require one to provide a contact email.
 - They ramble about needing this for reliable service.

I suppose I could come up with an user agent - though being in such an early stage of development I fear being blocked for sending repeated requests (Need them for  testing).


The whole idea that requiring to add an email address to improve the service seems suspicious.
I mean it's easy enough to automatically generate one - so spammers won't be limited, but as real person I'd fear my address might get abused.
I also think that such search requests contain sensitive information, so I definitely would not want that to be linked by default with a personal identification.


Currently I submit my requests manually - every few minutes.
I manage to get one response after about a minute, with some 503 errors mixed in.
I don't see how this would justify any blocking.
However with this response time it is all but useless for my intended application to retrieve DOIs for dozen or even 100s of references.



