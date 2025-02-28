#ifndef CLASSTAG_H
#define CLASSTAG_H

#include <regex>

#include "tagobject.h"

class ClassTag : public TagObject{
public:
  str getCleanAddress();
  str getClassName();

  ClassTag(TagObject aTagObject);

};





#endif //CLASSTAG_H