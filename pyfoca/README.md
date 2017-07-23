Introduction
===
If you're familiar with the Windows FOCA application, this is basically a python version of it. Pyfoca will use Google to discover files with extensions such as .pdf, .xls, .doc, etc. and download them. Once downloaded, it will extract all metadata which, in many cases, include usernames you can use for password attacks. 

Instructions
===
<br />
Usage menu:
<pre><code>
 -------------------------------------------------------------------------------
  pyfoca v1.6 - Document Metadata Extractor, Alton Johnson (alton.jx@gmail.com)
 -------------------------------------------------------------------------------

 Usage: ./pyfoca.py &lt;OPTIONS&gt;

 Domain options:

    -d &lt;domain&gt;      Harvests all documents from a domain (saves to pyfoca-downloads/).
				     Afterwards, extract metadata.

 Parse file/dir:

    -f &lt;file&gt;     Extracts metadata specifically from one file. (Cannot use with '-d')
    -w &lt;dir&gt;      Extracts metadata from files within specified directory. (Cannot use with '-d')

 Foca Export Parsing:

    -r &lt;directory&gt;      Parses data exported from FOCA. Provide directory containing exported files.

 Misc:

    -x                     After parsing metadata, delete files downloaded from the domain.
    -e &lt;pdf|doc|xls|all&gt;   Search based on provided extension(s). Separate with comma. (Default is all.)
    -p &lt;number&gt;            Searches x amount of google pages (per extension). (Default is 2.)
    -t &lt;secs&gt;              Sets timeout value. (Default is 5.)
    -v                     Prints status messages for files that are downloaded.

 Supported extensions are: .pdf, .doc, .docx, .xls, .xlsx, and .ppt
 Example: ./pyfoca.py -d www.domain.com -e pdf,doc -p 3
</code></pre>