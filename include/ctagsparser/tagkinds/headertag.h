#include <regex>
#include <filesystem>

#include "tagobject.h"


class HeaderTag : public TagObject{

public:    
    /// @brief Returns the name of the included module
    /// @return 
    str getCleanAddress();
    str getHeaderName();

    HeaderTag(TagObject aTagObject);

};